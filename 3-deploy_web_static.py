#!/usr/bin/python3
'''
Prototype: def deploy():
The script should take the following steps:
Call the do_pack() function and store the path of the created archive
Return False if no archive has been created
Call the do_deploy(archive_path) function,
using the new path of the new archive
Return the return value of do_deploy
'''
from fabric.api import run, put, env, local
import os
from datetime import datetime
hosts = ["100.26.239.81", "100.25.163.174"]
env.user = "ubuntu"


def do_pack():
    """create .tgz archive of web_static/ folder"""
    try:
        arch_name = "web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S'))
        local("mkdir -p versions")
        local("tar -cvzf versions/{} {}".format(
            arch_name, "web_static/"))
        return "versions/{}".format(arch_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploys archive to webservers"""
    if os.path.exists(archive_path):
        try:

            # Extract the filename without extension
            fileName = archive_path.split("/")[-1]

            # Upload the archive to /tmp/ directory on the web server
            put(archive_path, "/tmp/")

            # Create destination directory
            dest = ("/data/web_static/releases/" + fileName.split(".")[0])
            run("sudo mkdir -p {}".format(dest))

            # Extract the archive to the destination directory
            run("sudo tar -xzf /tmp/{} -C {}".format(fileName, dest))

            # Remove the archive from /tmp/
            run("sudo rm /tmp/{}".format(fileName))

            # move files to parent directory and remove now empty subdir...
            run("sudo mv {}/web_static/* {}/".format(dest, dest))
            run("sudo rm -rf {}/web_static".format(dest))

            # Remove the symbolic link /data/web_static/current
            run("sudo rm -rf /data/web_static/current")

            # Create a new symbolic link /data/web_static/current
            run("sudo ln -s {} /data/web_static/current".format(dest))

            return True
        except Exception as e:
            return False
    else:
        return False


def deploy():
    ''' controls the deployment'''
    try:
        archive = do_pack()
        if archive:
            for host in hosts:
                env.host_string = host  # Set the current host
                deployment = do_deploy(archive)
                if not deployment:
                    return False
                print("New version deployed!")
            return True
        else:
            return False
    except Exception as e:
        return False
