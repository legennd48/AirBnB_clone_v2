# Puppet manifest to set up a web server

# Installing Nginx
package { 'nginx':
  ensure => installed,
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
  ensure  => file,
  content => 'this is just a fake HTML for testing',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Give ownership of /data/ to ubuntu
file { '/data/':
  ensure  => directory,
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Configure Nginx server to serve the content of /data/web_static/current/ to hbnb_static
file_line { 'nginx_hbnb_static_config':
  path    => '/etc/nginx/sites-enabled/default',
  line    => '    location /hbnb_static/ {',
  before  => '    server_name _;',
  content => "        alias /data/web_static/current/;\n    }\n",
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  subscribe => File['/etc/nginx/sites-enabled/default'],
}
