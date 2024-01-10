#!/usr/bin/env bash
# sets up a web server and does the following:
# Install Nginx if it not already installed
# Create the folder /data/web_static/shared/ if it doesn’t already exist
# Create a fake HTML file /data/web_static/releases/test/index.html
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# Give ownership of the /data/ folder to the ubuntu user AND group
# pdate the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static

# installing Nginx
apt-get update
apt-get install -y nginx

# create folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# create fake index.html
echo "this is just a fake HTML for testing" > /data/web_static/releases/test/index.html

# create a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to ubuntu
chown -R ubuntu:ubuntu /data/

# configure Nginx server to to serve the conteent of /data/web_static/current/ to hbnb_static
cfg="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

sed -i "/server_name _;/ a$cfg" /etc/nginx/sites-enabled/default

service nginx restart
