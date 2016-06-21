#!/bin/bash

echo "Installing prerequisites"
sudo apt-get install -y sqlite3 libsqlite3-dev
sudo apt-get install -y libqt4-sql-sqlite

echo "Setting up database"
touch piwood.db
