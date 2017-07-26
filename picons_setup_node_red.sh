#!/bin/bash
# Pi-Cons Setup procedures.

usr=$(env | grep SUDO_USER | cut -d= -f 2)

if [ -z $usr ] && [ $USER = "root" ]
then
    echo "The script needs to run as root" && exit 1
fi

apt-get -y update
apt-get -y upgrade
apt-get -y install nodejs
npm install -g --unsafe-perm node-red
npm install node-red-contrib-ui
npm install node-red-node-serialport
npm install node-red-contrib-modbus


#cat /home/pi/PiCons/node_red_autostart.sh >> .bashrc
