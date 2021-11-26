#!/usr/bin/env python3

import json
import subprocess
import argparse

from os.path import expanduser


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


help_desc_msg = """
dbrestore

ex:
python dbrestore.py -t local -d ~/backup/aig
"""

help_epi_msg = """
end
"""

parser = argparse.ArgumentParser(description=help_desc_msg, epilog=help_epi_msg, formatter_class=HelpFormatter)

parser.add_argument("-d", "--backupdir", type=str, help="Directory Path (from)")
parser.add_argument("-t", "--target", type=str, help="Config Name. (to)")

args = parser.parse_args()


def config():
    json_open = open(expanduser('~/aig/backup.json'), 'r')
    json_load = json.load(json_open)

    backup_dir = args.backupdir
    config_name = args.target
    config = json_load[config_name]
    host = config['host']
    dbname = config['dbname']
    username = config['username']
    password = config['password']

    return host, dbname, username, password, expanduser(backup_dir)


def restore():
    host, dbname, username, password, backup_dir = config()
    if username:
        subprocess.run(["mongorestore", "--host", host, "--authenticationDatabase", dbname, "-u", username, "-p", password, "-d", dbname, backup_dir])
    else:
        subprocess.run(["mongorestore", "--host", host, "-d", dbname, backup_dir])


if __name__ == "__main__":
    try:
        restore()
    except Exception as e:
        print(e)
