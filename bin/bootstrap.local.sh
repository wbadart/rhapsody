#!/bin/sh

##
# bin/bootstrap.local.sh
#
# Script for quickly setting up your local app instance.
#
# Will Badart <netid:wbadart>
# created: MAR 2018
##

if ! which mysql > /dev/null; then
    echo 'ERROR: No command "mysql" found'
    exit 1
fi

if [ ! -f ./manage.py ]; then
    echo 'ERROR: Please run me from the project root directory'
    exit 1
fi

echo 'create rhapsody mysql user password:'
read -s pw
echo 'confirm:'
read -s pw1

if [ "$pw" != "$pw1" ]; then
    echo 'ERROR: Passwords do not match'
    exit 1
fi

mysql -u root <<EOF
CREATE DATABASE rhapsody CHARACTER SET UTF8;
CREATE USER rhapsody@localhost IDENTIFIED BY '$pw';
GRANT ALL PRIVILEGES ON rhapsody.* TO rhapsody@localhost;
FLUSH PRIVILEGES;
EOF

echo 'Migrating...'
./manage.py migrate

echo 'Creating django admin user...'
./manage.py createsuperuser

echo 'Seeding database...'
./manage.py import
