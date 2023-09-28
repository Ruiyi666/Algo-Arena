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
# install python and pip
apt-get install -y apt-utils
apt-get install -y python3 python3-pip
apt-get install -y pkg-config libmysqlclient-dev coreutils
cd /vagrant/
ls
pwd
cp -r backend ~
ls
pwd
cd ~/backend
ls
pwd
# install python dependencies
pip install pyOpenSSL --upgrade
# pip install -v --progress-bar on -r requirements.txt
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata /vagrant/database/data.json
# start the backend server by running the following command
# export DJANGO_SETTINGS_MODULE=backend.settings
# daphne backend.asgi:application
nohup python3 manage.py runserver 0.0.0.0:8000 &
