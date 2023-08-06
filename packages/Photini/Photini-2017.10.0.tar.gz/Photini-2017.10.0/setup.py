#!/usr/bin/env python
#  Photini - a simple photo metadata editor.
#  http://github.com/jim-easterbrook/Photini
#  Copyright (C) 2012-17  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
#  This program is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see
#  <http://www.gnu.org/licenses/>.

from datetime import date
from distutils.cmd import Command
from distutils.command.upload import upload
from distutils.errors import DistutilsExecError, DistutilsOptionError
import os
from setuptools import setup
import sys

# read current version info without importing package
with open('src/photini/__init__.py') as f:
    exec(f.read())

cmdclass = {}
command_options = {}

# get GitHub repo information
# requires GitPython - 'sudo pip install gitpython'
try:
    import git
except ImportError:
    git = None
if git:
    try:
        repo = git.Repo()
        if repo.is_dirty():
            dev_no = int(build.split()[0])
            commit = build.split()[1][1:-1]
            # increment dev_no when there's been a commit
            last_commit = str(repo.head.commit)[:7]
            if last_commit != commit:
                dev_no += 1
                commit = last_commit
            # get latest release tag
            latest = 0
            for tag in repo.tags:
                tag_name = str(tag)
                if tag.commit.committed_date < latest:
                    continue
                if tag_name[0] == 'v':
                    tag_name = tag_name[1:]
                if not tag_name.startswith('20'):
                    continue
                latest = tag.commit.committed_date
                last_release = tag_name
            # set current version number (calendar based)
            major, minor, micro = map(int, last_release.split('.'))
            today = date.today()
            if today.year == major and today.month == minor:
                micro += 1
            else:
                micro = 0
            __version__ = '{:4d}.{:d}.{:d}'.format(
                today.year, today.month, micro)
            # update __init__.py if anything's changed
            new_text = """from __future__ import unicode_literals

__version__ = '%s'
build = '%d (%s)'
""" % (__version__, dev_no, commit)
            with open('src/photini/__init__.py', 'r') as vf:
                old_text = vf.read()
            if new_text != old_text:
                with open('src/photini/__init__.py', 'w') as vf:
                    vf.write(new_text)
    except (git.exc.InvalidGitRepositoryError, git.exc.GitCommandNotFound):
        pass

# if sphinx is installed, add commands to build documentation and to
# extract strings for translation
try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
    command_options['build_sphinx'] = {
        'all_files'  : ('setup.py', '1'),
        'source_dir' : ('setup.py', 'src/doc'),
        'build_dir'  : ('setup.py', 'doc'),
        'builder'    : ('setup.py', 'html'),
        }
    cmdclass['gettext'] = BuildDoc
    command_options['gettext'] = {
        'all_files'  : ('setup.py', '1'),
        'source_dir' : ('setup.py', 'src/doc'),
        'build_dir'  : ('setup.py', 'src/lang/doc'),
        'builder'    : ('setup.py', 'gettext'),
        }
except ImportError:
    pass

# modify upload class to add appropriate tag
# requires GitPython - 'sudo pip install gitpython'
class upload_and_tag(upload):
    def run(self):
        import git
        message = 'Photini-' + __version__ + '\n\n'
        with open('CHANGELOG.txt') as cl:
            while not cl.readline().startswith('Changes'):
                pass
            while True:
                line = cl.readline().strip()
                if not line:
                    break
                message += line + '\n'
        repo = git.Repo()
        tag = repo.create_tag(__version__, message=message)
        remote = repo.remotes.origin
        remote.push(tags=True)
        return upload.run(self)
cmdclass['upload'] = upload_and_tag

# set options for building distributions
command_options['sdist'] = {
    'formats'        : ('setup.py', 'gztar'),
    'force_manifest' : ('setup.py', '1'),
    }

# add command to extract strings for translation
# NB the "babel" package provides an extract_messages command, but it is
# an alternative to xgettext, generating .pot files. This uses Qt's
# pylupdate5 (or pylupdate4) command to generate a .ts file
class extract_messages(Command):
    description = 'extract localizable strings from the project code'
    user_options = [
        ('output-file=', 'o',
         'name of the output file'),
        ('input-dir=', 'i',
         'directory that should be scanned for Python files'),
    ]

    def initialize_options(self):
        self.output_file = None
        self.input_dir = None

    def finalize_options(self):
        if not self.output_file:
            raise DistutilsOptionError('no output file specified')
        if not self.input_dir:
            raise DistutilsOptionError('no input directory specified')

    def run(self):
        inputs = []
        for name in os.listdir(self.input_dir):
            base, ext = os.path.splitext(name)
            if ext == '.py':
                inputs.append(os.path.join(self.input_dir, name))
        inputs.sort()
        out_dir = os.path.dirname(self.output_file)
        self.mkpath(out_dir)
        try:
            self.spawn(
                ['pylupdate5', '-verbose'] + inputs + ['-ts', self.output_file])
        except DistutilsExecError:
            self.spawn(
                ['pylupdate4', '-verbose'] + inputs + ['-ts', self.output_file])

cmdclass['extract_messages'] = extract_messages
command_options['extract_messages'] = {
    'output_file' : ('setup.py', 'src/lang/photini.ts'),
    'input_dir'   : ('setup.py', 'src/photini'),
    }

# add command to 'compile' translated messages
class build_messages(Command):
    description = 'compile translated strings (.ts) to binary .qm files'
    user_options = [
        ('output-dir=', 'o', 'location of output .qm files'),
        ('input-dir=', 'i', 'location of input .ts files'),
    ]

    def initialize_options(self):
        self.output_dir = None
        self.input_dir = None

    def finalize_options(self):
        if not self.output_dir:
            raise DistutilsOptionError('no output directory specified')
        if not self.input_dir:
            raise DistutilsOptionError('no input directory specified')

    def run(self):
        self.mkpath(self.output_dir)
        for name in os.listdir(self.input_dir):
            base, ext = os.path.splitext(name)
            if ext != '.ts' or '.' not in base:
                continue
            try:
                self.spawn(['lrelease-qt5', os.path.join(self.input_dir, name),
                            '-qm', os.path.join(self.output_dir, base + '.qm')])
            except DistutilsExecError:
                self.spawn(['lrelease', os.path.join(self.input_dir, name),
                            '-qm', os.path.join(self.output_dir, base + '.qm')])

cmdclass['build_messages'] = build_messages
command_options['build_messages'] = {
    'output_dir' : ('setup.py', 'src/photini/data/lang'),
    'input_dir'  : ('setup.py', 'src/lang'),
    }

data_files = []
if sys.platform.startswith('linux'):
    # install application menu shortcut
    data_files.append(('share/icons/hicolor/48x48/apps',
                       ['src/photini/data/icons/48/photini.png']))
    data_files.append(('share/applications', ['src/linux/photini.desktop']))
    command_options['install'] = {
        'single_version_externally_managed' : ('setup.py', '1'),
        'record'                            : ('setup.py', 'install.txt'),
        }

with open('README.rst') as ldf:
    long_description = ldf.read()
url = 'https://github.com/jim-easterbrook/Photini'

setup(name = 'Photini',
      version = __version__,
      author = 'Jim Easterbrook',
      author_email = 'jim@jim-easterbrook.me.uk',
      url = url,
      download_url = url + '/archive/' + __version__ + '.tar.gz',
      description = 'Simple photo metadata editor',
      long_description = long_description,
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Win32 (MS Windows)',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Graphics',
          ],
      packages = ['photini'],
      package_dir = {'' : 'src'},
      package_data = {
          'photini' : ['data/*.txt', 'data/*.png', 'data/icons/*/photini.png',
                       'data/*map/grey_marker.png', 'data/*map/script.js',
                       'data/lang/*.qm'],
          },
      data_files = data_files,
      cmdclass = cmdclass,
      command_options = command_options,
      entry_points = {
          'gui_scripts' : [
              'photini = photini.editor:main',
              ],
          },
      install_requires = ['appdirs >= 1.3', 'six >= 1.5'],
      extras_require = {
          'facebook' : ['requests-oauthlib >= 0.4', 'requests-toolbelt >= 0.4',
                        'keyring >= 7.0', 'Pillow >= 2.0'],
          'flickr'   : ['flickrapi >= 2.0', 'keyring >= 7.0'],
          'google'   : ['requests-oauthlib >= 0.4', 'keyring >= 7.0'],
          'importer' : ['gphoto2 >= 0.10'],
          'picasa'   : ['requests-oauthlib >= 0.4', 'keyring >= 7.0',
                        'certifi >= 2017.1'],
          'spelling' : ['pyenchant >= 1.6'],
          },
      zip_safe = False,
      )
