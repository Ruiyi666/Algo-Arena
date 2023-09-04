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
sudo apt-get install -y apache2 php libapache2-mod-php php-mysql
# install nodejs and npm to build the project
wget https://nodejs.org/dist/v18.17.1/node-v18.17.1-linux-x64.tar.xz
tar -xf node-v18.17.1-linux-x64.tar.xz
sudo cp -R node-v18.17.1-linux-x64/* /usr/
node -v
npm -v
cd /vagrant/
cp -r frontend ~
cd ~/frontend
rm -r node_modules
npm install
npm run build
# now copy the built files to the webserver
cp -r dist/* /var/www/html/

# Change VM's webserver's configuration to use shared folder.
# (Look inside test-website.conf for specifics.)
sudo cp /vagrant/website.conf /etc/apache2/sites-available/

# activate our website configuration ...
sudo a2ensite website
# ... and disable the default website provided with Apache
sudo a2dissite 000-default
# Restart the webserver, to pick up our configuration changes
sudo service apache2 restart
