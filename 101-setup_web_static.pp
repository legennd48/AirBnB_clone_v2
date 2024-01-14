# Puppet manifest to set up a web server

# Nginx configuration file
$conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"


# Installing Nginx
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

# Create folders
file { '/data/web_static/releases/test/':
  ensure => directory,
}

file { '/data/web_static/shared/':
  ensure => directory,
}

# Create fake index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'this is just a fake HTML for testing',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Give ownership of /data/ to ubuntu
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Configure Nginx server to serve the content of /data/web_static/current/ to hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $conf
} ->

# Restart Nginx service
exec { 'nginx restart':
  path => '/etc/init.d/'
}
