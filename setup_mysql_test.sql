-- Prepares a MySQL server for the project:
-- Grants specific permissions for user

-- Create a database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a user and set the password
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to the user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
