#!/bin/bash
# Pi-Cons Setup procedures.

usr=$(env | grep SUDO_USER | cut -d= -f 2)

if [ -z $usr ] && [ $USER = "root" ]
then
    echo "The script needs to run as root" && exit 1
fi

apt-get -y update
apt-get -y upgrade
apt-get install build-essential python-dev python-smbus git php-cli rng-tools chromium-browser -y
pip install mcp3008
pip install dicttoxml
cd /home/pi
chmod -R +x /home/pi/PiCons
cd /home/pi/.config/
mkdir autostart
cp /home/pi/PiCons/autoChromium.desktop /home/pi/.config/autostart/autoChromium.desktop
echo "@reboot php -S localhost:80 -t /home/pi/PiCons/ 2>&1 &" > cron.res
#echo "@reboot bash /home/pi/PiCons/picons_autostart.sh" >> cron.res
#echo "* * * * * php /home/pi/PiCons/watchDog.php" >> cron.res
crontab cron.res
rm cron.res
echo "You should restart the system."
echo "Type: sudo reboot"
reboot
