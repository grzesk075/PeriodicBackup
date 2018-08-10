#!/usr/bin/python

"""
Python3 tool for making data backups in zip files and copying them to indicated folders.
Source folders or files to copy along with destination folders for zip backup file
and placed in periodic_backup.ini config file.
This tool creates and overwrites one backup file per configured period (the default is a month).
Primary zip file is created in working directory next to ini file.
The name of directory should describe the purpose and content of copy.
"""

__version__ = '1.0.0'
__author__ = 'Grzegorz Kuprianowicz <grzesk075@gmail.com>'

import os

# config
PERIODS = ['day', 'month']
period = None
includes = None
excludes = None
copydirs = None

# Primary zip file absolute path
backupFilePath = None


def parse_config():
    import configparser
    config = configparser.ConfigParser()
    config.read('periodic_backup.ini')

    global period, includes, excludes, copydirs

    period = config['params']['period']
    if period not in PERIODS:
        raise Exception("Config param 'period' must be in " + str(PERIODS) + " but is '" + period + "'.")

    includes = config['input']['includes']
    excludes = config['input']['excludes']
    copydirs = config['output']['copydirs']


def assign_backup_file():
    import datetime
    now = datetime.datetime.now()
    day = '_{:02}'.format(now.day) if period == 'day' else ''
    file_name = 'backup_{0}_{1:02}{2}.zip'.format(now.year, now.month, day)

    global backupFilePath
    backupFilePath = os.path.abspath(file_name)  # in working dir


def get_paths_from_pattern(patterns):
    import glob
    paths = []
    for pattern in patterns.split(','):
        paths.extend(glob.glob(pattern, recursive=True))
    return paths

def zip_files():
    import zipfile
    includes_paths = get_paths_from_pattern(includes)
    excludes_paths = get_paths_from_pattern(excludes)
    print('Open archive ' + backupFilePath)
    with zipfile.ZipFile(backupFilePath, 'w') as zip_file:
        for file_path in includes_paths:
            if file_path in excludes_paths:
                print('Exclude ' + file_path)
                continue
            print('Add ' + file_path)
            zip_file.write(file_path)


def copy_backup():
    if not copydirs:
        return
    from shutil import copy
    for dir in copydirs.split(','):
        print('Copy {} to {}'.format(backupFilePath, dir))
        copy(backupFilePath, dir)


def print_usage():
    print(__doc__)


# main
print_usage()
parse_config()
assign_backup_file()
zip_files()
copy_backup()
