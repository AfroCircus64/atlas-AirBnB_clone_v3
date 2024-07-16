#!/bin/bash
set -e
# entrypoint.sh

# Check if MySQL is running
if pgrep mysqld > /dev/null
then
    echo "MySQL is already running"
else
    # Start MySQL service
    service mysql start

    # Wait for MySQL to start
    sleep 5

    # Create the MySQL database and user if they don't exist
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS $HBNB_MYSQL_DB;"
    mysql -u root -e "CREATE USER IF NOT EXISTS '$HBNB_MYSQL_USER'@'localhost' IDENTIFIED BY '$HBNB_MYSQL_PWD';"
    mysql -u root -e "GRANT ALL PRIVILEGES ON $HBNB_MYSQL_DB.* TO '$HBNB_MYSQL_USER'@'localhost';"
    mysql -u root -e "FLUSH PRIVILEGES;"
fi


export PYTHONPATH=/usr/src/app


# Execute the passed command
exec "$@" || tail -f /dev/null