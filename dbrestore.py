#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess
from os.path import expanduser


def config():
    home = expanduser("~")
    json_open = open('config/backup.json', 'r')
    json_load = json.load(json_open)

    host = json_load['host']
    dbname = json_load['dbname']
    username = json_load['username']
    password = json_load['password']
    backup_dir = json_load['backup_dir']
    return host, dbname, username, password, home + backup_dir


def restore():
    host, dbname, username, password, backup_dir = config()
    subprocess.run(["mongorestore", "--host", host, "--authenticationDatabase", dbname, "-u", username, "-p", password, "-d", dbname, backup_dir + "/" + dbname])


if __name__ == "__main__":
    restore()
