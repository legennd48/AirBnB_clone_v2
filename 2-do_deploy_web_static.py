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
env.hosts = ['100.26.239.81', '54.165.171.31']
env.user = 'ubuntu'


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
            print("Error: {}".format(e))
            return False
    else:
        return False
