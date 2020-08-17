#!/bin/bash

apt-get update -y
apt-get upgrade -y

apt-get install build-essential python-dev python-smbus git php-cli rng-tools chromium-browser -y

pip install dicttoxml

cd /home/pi
chmod -R +x /home/pi/PiCons

cd /home/pi/.config/
mkdir autostart
cp /home/pi/PiCons/autoChromium.desktop /home/pi/.config/autostart/autoChromium.desktop

echo "@reboot php -S localhost:80 -t /home/pi/PiCons/ 2>&1 &" > cron.res
echo "@reboot php -S localhost:8181 -t /home/pi/PiCons/StartPageWebroot/ 2>&1 &" >> cron.res
#echo "@reboot bash /home/pi/PiCons/picons_autostart.sh" >> cron.res
#echo "* * * * * php /home/pi/PiCons/watchDog.php" >> cron.res
crontab cron.res
rm cron.res
reboot
