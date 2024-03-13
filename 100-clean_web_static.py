#!/usr/bin/python3
import os
from fabric.api import *

env.hosts = ['54.236.27.34', '54.167.176.115']


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    """
    number = int(number)

    if number < 1:
        number = 1  # Keep at least one archive

    # Local cleanup
    local_archives = sorted(os.listdir("versions"))
    local_archives_to_remove = local_archives[:-number]
    with lcd("versions"):
        for archive in local_archives_to_remove:
            local("rm ./{}".format(archive))

    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        remote_archives_to_remove = remote_archives[:-number]
        for archive in remote_archives_to_remove:
            run("rm -rf ./{}".format(archive))
