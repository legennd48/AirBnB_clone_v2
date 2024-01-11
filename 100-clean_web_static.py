#!/usr/bin/python3
'''
Prototype: def deploy():
The script should take the following steps:
Call the do_pack() function and store the path of the created archive
Return False if no archive has been created
Call the do_deploy(archive_path) function,
using the new path of the new archive
Return the return value of do_deploy
do_clean(n=0): removes old versions and keeps n (or 1) newest versions only
'''
from fabric.api import run, put, env, local
import os
from datetime import datetime
from fabric.context_managers import lcd
env.hosts = ["100.26.239.81", "54.165.171.31"]


def do_pack():
    """create .tgz archive of web_static/ folder"""
    try:
        arch_name = "web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S'))
        local("mkdir -p versions/")
        local("tar -cvzf versions/{} -C {} .".format(
            arch_name, "web_static/"))
        return "versions/{}".format(arch_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploys archive to webservers"""
    if os.path.exists(archive_path):
        try:

            # Extract the filename without extension
            fileName = os.path.splitext(os.path.basename(archive_path))[0]

            # Upload the archive to /tmp/ directory on the web server
            put(archive_path, "/tmp/{}.tgz".format(fileName))

            # Create destination directory
            destination = "/data/web_static/releases/{}".format(fileName)
            run("mkdir -p {}".format(destination))

            # Extract the archive to the destination directory
            run("tar -xzf /tmp/{}.tgz -C {}".format(fileName, destination))

            # Remove the archive from /tmp/
            run("rm -rf /tmp/{}.tgz".format(fileName))

            # Remove the symbolic link /data/web_static/current
            run("rm -rf /data/web_static/current")

            # Create a new symbolic link /data/web_static/current
            run("ln -s {}/ /data/web_static/current".format(destination))

            return True
        except Exception as e:
            return False
    else:
        return False


def do_clean(number=0):
    num = 1 if int(number) == 0 else int(number)

    local_files = sorted(os.listdir("versions"))
    [local_files.pop() for i in range(num)]
    os.chdir("versions")
    [os.remove(j) for j in local_files]

    os.chdir("..")

    remote_files = run("ls -tr /data/web_static/releases").split()
    remote_files = [j for j in remote_files if "web_static_" in j]
    [remote_files.pop() for i in range(num)]
    [run("sudo rm -rf ./{}".format(j)) for j in remote_files]
