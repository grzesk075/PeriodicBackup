#!/usr/bin/python

"""
Python3 tool for making data backups in zip files and copying them to indicated folders.
Source folders or files to copy along with destination folders for zip backup file
and placed in periodic_backup.ini config file.
This tool creates and overwrites one backup file per configured period (the default is a month).
"""

__version__ = '1.0.0'
__author__ = 'Grzegorz Kuprianowicz <grzesk075@gmail.com>'

# config
PERIODS = ['day', 'month']
period = None

def parse_config():
    import configparser
    config = configparser.ConfigParser()
    config.read('periodic_backup.ini')

    period = config['params']['period']
    if period not in PERIODS:
        raise Exception("Config param 'period' must be in " + str(PERIODS) + " but is '" + period + "'.")


def print_usage():
    print(__doc__)
    print()


# main
print_usage()
parse_config()
