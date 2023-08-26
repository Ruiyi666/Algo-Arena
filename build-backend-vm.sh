#!/bin/bash

# allow services to run
echo exit 0 > /usr/sbin/policy-rc.d
chmod +x /usr/sbin/policy-rc.d

# Ensure that packages do not request user input from console.
export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
# Set timezone options without needing to interact with console.
echo "tzdata tzdata/Areas select Pacific" | debconf-set-selections
echo "tzdata tzdata/Zones/Europe select Auckland" | debconf-set-selections

apt-get update
apt-get install -y apache2 php libapache2-mod-php php-mysql
# install python and pip
apt-get install -y python3 python3-pip
cd /vagrant/backend
# install python dependencies
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate


# start the backend server by running the following command
daphne backend.asgi:application
