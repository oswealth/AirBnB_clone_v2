#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from os import path


env.hosts = ['54.236.27.34', '54.167.176.115']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not path.exists(archive_path):
        print(f"Error: Archive '{archive_path}' not found.")
        return False

    try:
        # Upload the archive to the temporary folder on the server
        put(archive_path, '/tmp/')

        # Extract the archive
        timestamp = archive_path.split('_')[-1][:-4]
        remote_path = '/data/web_static/releases/web_static_{}/'.format(timestamp)

        run('sudo mkdir -p {}'.format(remote_path))
        run('sudo tar -xzf /tmp/{} -C {}'.format(path.basename(archive_path), remote_path))

        # Remove the temporary archive
        run('sudo rm /tmp/{}'.format(path.basename(archive_path)))

        # Move contents into the web_static release folder
        run('sudo mv {}web_static/* {}'.format(remote_path, remote_path))

        # Remove the extraneous web_static directory
        run('sudo rm -rf {}web_static'.format(remote_path))

        # Update the symbolic link
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(remote_path))

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print(f"Error during deployment: {e}")
        return False
