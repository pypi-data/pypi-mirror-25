#!/usr/bin/env python
import contextlib
import imp
import os
import re
import subprocess
import sys

from setuptools import setup
from setuptools.command.sdist import sdist

VERSION_FILE = 'ebosia/version.py'

def _get_output_or_none(args):
    try:
        return subprocess.check_output(args).decode('utf-8').strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def _get_git_description():
    return _get_output_or_none(['git', 'describe'])

def _get_git_branches_for_this_commit():
    branches = _get_output_or_none(['git', 'branch', '-r', '--contains', 'HEAD'])
    split = branches.split('\n') if branches else []
    return [branch.strip() for branch in split]

def _is_on_releasable_branch(branches):
    return any([branch == 'origin/master' or branch.startswith('origin/hotfix') for branch in branches])

def _git_to_version(git):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git)
    if not match:
        version = git
        branch = None
    else:
        branch = os.environ.get('GIT_BRANCH', None)
        version = "{tag}.post{offset}".format(**match.groupdict())
    print("Calculated ebosia version '{}' from git description '{}' and branch '{}'".format(version, git, branch))
    return version

def _get_version_from_git():
    git_description = _get_git_description()
    git_branches = _get_git_branches_for_this_commit()
    version = _git_to_version(git_description) if git_description else None
    if git_branches and not _is_on_releasable_branch(git_branches):
        sys.stderr.write((
            "Forcing version to 0.0.1 because this commit is on branches {} "
            "and not a whitelisted branch\n").format(git_branches))
        version = '0.0.1'
    return version

VERSION_REGEX = re.compile(r'__version__ = "(?P<version>[\w\.]+)"')
def _get_version_from_file():
    with open(VERSION_FILE, 'r') as f:
        content = f.read()
    match = VERSION_REGEX.match(content)
    if not match:
        raise Exception("Failed to pull version out of '{}'".format(content))
    version = match.group(1)
    return version


@contextlib.contextmanager
def write_version():
    version = _get_version_from_git()
    if version:
        with open(VERSION_FILE, 'r') as version_file:
            old_contents = version_file.read()
        with open(VERSION_FILE, 'w') as version_file:
            new_contents = '__version__ = "{}"\n'.format(version)
            version_file.write(new_contents)
    print('version found {}'.format(version))
    yield
    if version:
        with open(VERSION_FILE, 'w') as f:
            f.write(old_contents)
        print("Re-wrote old contents back to {}".format(VERSION_FILE))

def get_version():
    file_version = _get_version_from_file()
    git_version = _get_version_from_git()
    return git_version if file_version == 'development' else file_version

class CustomSDistCommand(sdist): # pylint: disable=no-init
    def run(self):
        with write_version():
            sdist.run(self)

def main():
    setup(
        name                = 'ebosia',
        version             = get_version(),
        description         = "A library for getting events throughout the system",
        long_description    = open('README.md').read(),
        author              = 'Authentise, Inc.',
        author_email        = 'engineering@authentise.com',
        cmdclass            = {
            'sdist'         : CustomSDistCommand,
        },
        entry_points        = {
            'pytest11'      : [
                'ebosia = ebosia.fixtures'
            ]
        },
        extras_require      = {
            'develop'       : [
                'coverage>=3.7.1',
                'mothermayi==0.4',
                'mothermayi-pylint==0.5',
                'mothermayi-isort==0.5',
                'pylint>=1.5.2',
                'pytest>=2.8.5',
                'pytest-asyncio==0.1.3',
                'pytest-cov>=1.8.1',
                'pytest-mock==1.5.0',
            ]
        },
        install_requires    = [
            'aioamqp-authentise==0.10.1',
            'kombu==3.0.34', # sepiida.celery uses kombu 3.0.34
        ],
        packages            = ['ebosia'],
        package_data        = {
            'ebosia'      : ['ebosia/*'],
        },
        scripts             = [
            'bin/async-emitter',
            'bin/async-subscribe',
            'bin/sync-emitter',
            'bin/sync-subscribe',
        ],
        include_package_data= True,
    )

if __name__ == '__main__':
    main()
