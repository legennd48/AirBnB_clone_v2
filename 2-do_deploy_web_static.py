#!/usr/bin/python3
'''
distributes an archive to web servers, using the function do_deploy:
Prototype: def do_deploy(archive_path):
Returns False if the file at the path archive_path doesn’t exist
Upload the archive to the /tmp/ directory of the web server
Uncompress the archive to the folder /data/web_static/releases/
<archive filename without extension> on the web server
Delete the archive from the web server
Delete the symbolic link /data/web_static/current from the web server
Create a new the symbolic link /data/web_static/current on the web server,
linked to the new version of your code (/data/web_static/releases/<archive
filename without extension>)
'''
from fabric.api import run, put, env
import os
env.hosts = ['100.26.239.81', '100.25.163.174']
env.user = "ubuntu"


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
