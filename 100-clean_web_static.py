#!/usr/bin/python3
"""
performs cleaning after update
cleaninf is done locally and then remotely
"""
from fabric.api import *
import os.path
import os
env.user = "ubuntu"
hosts = ["100.26.239.81", "100.25.163.174"]


def do_clean(number=0):
    number = 1 if int(number) == 0 else int(number)

    files = sorted(os.listdir("versions"))
    [files.pop() for i in range(number)]
    with lcd("versions"):
        for j in files:
            local("rm ./{}".format(j))

    for host in hosts:
        env.host_string = host
        with cd("/data/web_static/releases"):
            files = run("ls -tr").split()
            files = [j for j in files if "web_static_" in j]
            [files.pop() for i in range(number)]
            for j in files:
                run("sudo rm -rf ./{}".format(j))
