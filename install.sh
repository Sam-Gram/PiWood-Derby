#!/bin/bash

echo "Installing prerequisites"
sudo apt-get -y update
sudo apt-get install -y build-essential python-dev
sudo apt-get install -y python-smbus python-imaging
sudo apt-get install -y python-pyside
sudo apt-get install -y sqlite3 libsqlite3-dev
sudo apt-get install -y libqt4-sql-sqlite
curl -O -L https://github.com/adafruit/Adafruit_Python_LED_Backpack/archive/master.zip
unzip master.zip
(cd Adafruit_Python_LED_Backpack-master; sudo python setup.py install;)



echo "Setting up database"
touch piwood.db
python installDatabase.py
