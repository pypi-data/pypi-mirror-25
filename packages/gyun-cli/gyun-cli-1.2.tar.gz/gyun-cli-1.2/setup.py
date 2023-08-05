# coding:utf-8

import os
import sys
import platform
from setuptools import setup, find_packages

config_sample = '''
qy_access_key_id: 'GYUNACCESSKEYID'
qy_secret_access_key: 'GYUNSECRETACCESSKEYEXAMPLE'
zone: 'ZONEID'
'''

def is_windows():
    return platform.system().lower() == 'windows'

def prepare_config_file():
    config_file = os.path.expanduser('~/.gyun/config.yaml')
    if os.path.exists(config_file):
        return

    d = os.path.dirname(config_file)
    if not os.path.exists(d):
        os.makedirs(d)

    with open(config_file, 'w') as fd:
        fd.write(config_sample)

def setup_gyun_completer():
    # only support linux
    if is_windows():
        return

    cmd = 'complete -C gyun_completer gyun'
    complete_file = '/etc/bash_completion.d/gyun-cli'
    complete_dir = os.path.dirname(complete_file)
    if os.path.exists(complete_dir) and os.access(complete_dir, os.W_OK):
        with open((complete_file), 'w') as fd:
            fd.write(cmd)
    else:
        with open(os.path.expanduser('~/.bash_profile'), 'a') as fd:
            fd.write('\n\n# GYUN CLI\n%s\n' % cmd)


if len(sys.argv) < 2 or sys.argv[1] != 'install':
    bin_scripts = ['bin/gyun', 'bin/gyun.cmd', 'bin/gyun_completer']
elif is_windows():
    bin_scripts = ['bin/gyun.cmd']
else:
    bin_scripts = ['bin/gyun', 'bin/gyun_completer']

setup(
    name = 'gyun-cli',
    version = '1.2',
    description = 'Command Line Interface for GYUN.',
    long_description = open('README.rst', 'rb').read().decode('utf-8'),
    keywords = 'gyun iaas gomestor cli',
    author = 'GYUN Team',
    author_email = 'service@gomeholdings.com',
    url = 'http://docs.qc.gyun.com',
    scripts=bin_scripts,
    packages = find_packages('.'),
    package_dir = {'gyun-cli': 'gyun'},
    namespace_packages = ['gyun'],
    include_package_data = True,
    install_requires = [
        'argparse>=1.1',
        'PyYAML>=3.1',
        'gyun-sdk>=1.1',
    ]
)

if len(sys.argv) >= 2 and sys.argv[1] == 'install':
    prepare_config_file()
    setup_gyun_completer()
