#!/bin/bash

while getopts ":h:n:u:p:" opt; do
  case $opt in
    h) DB_HOST="$OPTARG" ;;
    n) DB_NAME="$OPTARG" ;;
    u) DB_USER="$OPTARG" ;;
    p) DB_PASSWORD="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done

echo "Database Host: $DB_HOST"
echo "Database User: $DB_USER"
echo "Database Name: $DB_NAME"
echo "Database Password: $DB_PASSWORD"

# allow services to run
sudo echo exit 0 > /usr/sbin/policy-rc.d
sudo chmod +x /usr/sbin/policy-rc.d

# Ensure that packages do not request user input from console.
export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
# Set timezone options without needing to interact with console.
echo "tzdata tzdata/Areas select Pacific" | debconf-set-selections
echo "tzdata tzdata/Zones/Europe select Auckland" | debconf-set-selections

sudo apt-get update
# install python and pip
sudo apt-get install -y apt-utils python3 python3-pip python3-venv
sudo apt-get install -y pkg-config libmysqlclient-dev coreutils

if [ ! -d "~/backend" ]; then
    cp -r /vagrant/backend ~
fi
if [ ! -d "~/database" ]; then
    cp -r /vagrant/database ~
fi
cd ~/backend
python3 -m venv my_env
source my_env/bin/activate
# install python dependencies
pip install pyOpenSSL --upgrade
# pip install -i https://mirrors.aliyun.com/pypi/simple pyOpenSSL --upgrade
pip install -r requirements.txt
# pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

# start the backend server by running the following command

# add those to os environment
# export DB_HOST=$DB_HOST
# export DB_USER=$DB_USER
# export DB_NAME=$DB_NAME
# export DB_PASSWORD=$DB_PASSWORD
touch ~/daphne.log
rm .env
echo "DB_HOST=$DB_HOST" >> .env
echo "DB_USER=$DB_USER" >> .env
echo "DB_NAME=$DB_NAME" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata ~/database/data.json
nohup daphne -b 0.0.0.0 -p 8000 backend.asgi:application &> ~/daphne.log &
ps aux | grep daphne
