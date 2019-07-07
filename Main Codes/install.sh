#!/bin/bash

NPM_INSTALL="sudo npm i formidable cors express"
PY_INSTALL="sudo -H python3 -m pip install pyserial"

installNode()
{
    sudo apt install curl python-software-properties
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    sudo apt update
    sudo apt install nodejs
}

if [ $(id -u) != "0" ]; then
    echo "You must be the superuser to run this script" >&2
    exit 1
else
    echo -e "\n"
fi

echo "Checking for Python3 ..."
dpkg -s python3 &> /dev/null
if [ $? -eq 0 ]; then
    echo -e "Python3 already installed.\n"
else
    echo -e "Please install python3 to continue\n"
    exit 1
fi

echo "Checking for NodeJS ..."
dpkg -s nodejs &> /dev/null
if [ $? -eq 0 ]; then
    echo -e "NodeJS already installed.\n"
else
    echo "NodeJS is not installed. Installing..."
    installNode
    echo -e "NodeJS installed Successfully.\n"
fi

echo "Checking for NPM ..."
dpkg -s npm &> /dev/null
if [ $? -eq 0 ]; then
    echo -e "NPM already installed.\n"
else
    echo "NPM is not installed. Installing..."
    sudo apt install npm
    echo -e "NPM installed Successfully.\n"
fi

$NPM_INSTALL
$PY_INSTALL