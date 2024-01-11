#!/usr/bin/python3
'''
Fabric script that generates a .tgz from the content of
/web-stack/ using the function do_pack
'''
from fabric.api import local
from datetime import datetime

def do_pack():
    try:
        arch_name = "web_static_{}.tgz".format(datetime.now().strftime('%Y%m%d%H%M%S'))
        local("mkdir -p ./versions/")
        local("tar -cvzf ./versions/{} -C {} .".format(arch_name, "./web_static"))
        return "./versions/{}".format(arch_name)
    except Exception as e:
        return None
