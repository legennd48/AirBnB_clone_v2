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
    """
    Deploy archive to web server
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except:
        return False
