#!/bin/bash

while getopts ":n:u:p:" opt; do
  case $opt in
    n) DB_NAME="$OPTARG" ;;
    u) DB_USER="$OPTARG" ;;
    p) DB_PASSWORD="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done

# allow services to run
echo exit 0 > /usr/sbin/policy-rc.d
chmod +x /usr/sbin/policy-rc.d

# Update Ubuntu software packages.
apt-get update
apt-get install -y apt-utils
      
# We create a shell variable MYSQL_PWD that contains the MySQL root password
export MYSQL_PWD=$DB_PASSWORD

# If you run the `apt-get install mysql-server` command
# manually, it will prompt you to enter a MySQL root
# password. The next two lines set up answers to the questions
# the package installer would otherwise ask ahead of it asking,
# so our automated provisioning script does not get stopped by
# the software package management system attempting to ask the
# user for configuration information.
echo "mysql-server mysql-server/root_password password $DB_PASSWORD" | debconf-set-selections 
echo "mysql-server mysql-server/root_password_again password $DB_PASSWORD" | debconf-set-selections

# Install the MySQL database server.
apt-get -y install mysql-server
# On normal VMs MySQL server will now be running, but starting
# the service explicitly even if it's started causes no warnings.
# (... and it _is_ necessary for some Docker testing I'm doing)
service mysql start

# Run some setup commands to get the database ready to use.
# First create a database.
# echo "CREATE DATABASE algo_arena_db;" | mysql
echo "CREATE DATABASE $DB_NAME;" | mysql

# Then create a database user "algo_arena_db_user" with the given password.
# echo "CREATE USER 'algo_arena_db_user'@'%' IDENTIFIED BY 'algo_arena_db_password';" | mysql
echo "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';" | mysql

# Grant all permissions to the database user "algo_arena_db_user" regarding
# the "algo_arena_db" database that we just created, above.
# echo "GRANT ALL PRIVILEGES ON algo_arena_db.* TO 'algo_arena_db_user'@'%'" | mysql
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%'" | mysql

# ... and run all of the SQL within the setup-database.sql file,
# which is part of the repository containing this Vagrantfile, so you
# can look at the file on your host. The mysql command specifies both
# the user to connect as (algo_arena_db_user) and the database to use (algo_arena_db).
# cat /vagrant/setup-database.sql | mysql -u algo_arena_db_user algo_arena_db

# By default, MySQL only listens for local network requests,
# i.e., that originate from within the dbserver VM. We need to
# change this so that the webserver VM can connect to the
# database on the dbserver VM. Use of `sed` is pretty obscure,
# but the net effect of the command is to find the line
# containing "bind-address" within the given `mysqld.cnf`
# configuration file and then to change "127.0.0.1" (meaning
# local only) to "0.0.0.0" (meaning accept connections from any
# network interface).
sed -i'' -e '/bind-address/s/127.0.0.1/0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# We then restart the MySQL server to ensure that it picks up
# our configuration changes.
service mysql restart
