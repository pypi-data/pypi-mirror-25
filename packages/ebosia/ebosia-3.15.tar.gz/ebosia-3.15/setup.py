#!/usr/bin/env python
import contextlib
import imp
import os
import re

from setuptools import setup


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

@contextlib.contextmanager
def write_version():
    VERSION_FILE = 'ebosia/version.py'
    git_description = os.environ.get('GITDESCRIPTION', None)
    version = _git_to_version(git_description) if git_description else None
    print('version found {}'.format(version))
    if version:
        with open(VERSION_FILE, 'r') as f:
            old_contents = f.read()
        print("Read version {} from original version file {}".format(old_contents, VERSION_FILE))
        with open(VERSION_FILE, 'w') as f:
            new_contents = 'VERSION = "{}"\n'.format(version)
            f.write(new_contents)
        print("Wrote {} to {}".format(new_contents, VERSION_FILE))
    yield
    if version:
        with open(VERSION_FILE, 'w') as f:
            f.write(old_contents)
        print("Re-wrote old contents back to {}".format(VERSION_FILE))

def get_version():
    basedir = os.path.abspath(os.path.dirname(__file__))
    version = imp.load_source('version', os.path.join(basedir, 'ebosia', 'version.py'))
    return version.VERSION

def main():
    with write_version():
        setup(
            name                = 'ebosia',
            version             = get_version(),
            description         = "A library for getting events throughout the system",
            long_description    = open('README.md').read(),
            author              = 'Authentise, Inc.',
            author_email        = 'engineering@authentise.com',
            entry_points        = {
                'pytest11'      : [
                    'ebosia = ebosia.fixtures'
                ]
            },
            extras_require      = {
                'develop'       : [
                    'coverage==3.7.1',
                    'mothermayi==0.4',
                    'mothermayi-pylint==0.5',
                    'mothermayi-isort==0.5',
                    'pylint==1.5.2',
                    'pytest==2.8.5',
                    'pytest-asyncio==0.1.3',
                    'pytest-cov==1.8.1',
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
