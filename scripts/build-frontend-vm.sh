#!/bin/bash

while getopts ":h:p:" opt; do
  case $opt in
    h) BK_HOST="$OPTARG" ;;
    p) BK_PORT="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done

# allow services to run
sudo echo exit 0 > /usr/sbin/policy-rc.d
sudo chmod +x /usr/sbin/policy-rc.d

# Ensure that packages do not request user input from console.
export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
# Set timezone options without needing to interact with console.
echo "tzdata tzdata/Areas select Pacific" | debconf-set-selections
echo "tzdata tzdata/Zones/Europe select Auckland" | debconf-set-selections

sudo apt-get update
sudo apt-get install -y apt-utils
sudo apt-get install -y apache2
# install nodejs and npm to build the project
# wget https://nodejs.org/dist/v18.17.1/node-v18.17.1-linux-x64.tar.xz
# tar -xf node-v18.17.1-linux-x64.tar.xz
# sudo cp -R node-v18.17.1-linux-x64/* /usr/
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
npm -v
# if not exist frontend folder, copy it
if [ ! -d "~/frontend" ]; then
    cp -r /vagrant/frontend ~
fi
cd ~/frontend

rm -r node_modules
npm install

rm .env
echo "VITE_APP_BACKEND_HOST=$BK_HOST" >> .env
echo "VITE_APP_BACKEND_PORT=$BK_PORT" >> .env

npm run build
# now copy the built files to the webserver
sudo cp -r dist/* /var/www/html/

# Change VM's webserver's configuration to use shared folder.
# (Look inside test-website.conf for specifics.)
sudo cp website.conf /etc/apache2/sites-available/

# activate our website configuration ...
sudo a2ensite website
# ... and disable the default website provided with Apache
sudo a2dissite 000-default
# Restart the webserver, to pick up our configuration changes
sudo service apache2 restart
