#!/usr/bin/python3
"""Compress web static package"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['54.236.27.34', '54.167.176.115']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(timestamp))

        run('sudo tar -xzf /tmp/web_static_{}.tgz -C '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
            .format(timestamp))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/web_static_{}/ '
            '/data/web_static/current'.format(timestamp))
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False

    return True
