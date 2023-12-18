-- prepares a MySQL server for the project
-- Grant s permissions to user 'hbnh_dev'

-- Create a new database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a user and set the password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database to the user
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to the user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
