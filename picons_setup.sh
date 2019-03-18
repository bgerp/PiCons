#!/bin/bash
# Pi-Cons Setup procedures.

usr=$(env | grep SUDO_USER | cut -d= -f 2)

if [ -z $usr ] && [ $USER = "root" ]
then
    echo "The script needs to run as root" && exit 1
fi

apt-get -y update
apt-get -y upgrade
apt-get install build-essential python-dev python-smbus git php-cli
cd /home/pi/Downloads/
mkdir libs
cd libs
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008/
python setup.py install
pip install dicttoxml
cd /home/pi
chmod 0777 /home/pi/PiCons/
wget -qO - http://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add –
echo "deb http://dl.bintray.com/kusti8/chromium-rpi jessie main" | sudo tee -a /etc/apt/sources.list
apt-get -y update
apt-get -y install chromium-browser
cd /home/pi/.config/
mkdir autostart
cp /home/pi/PiCons/autoChromium.desktop /home/pi/.config/autostart/autoChromium.desktop
echo "@reboot php -S localhost:8181 -t /home/pi/PiCons/StartPageWebroot" > cron.res
echo "@reboot bash /home/pi/PiCons/picons_autostart.sh" >> cron.res
crontab cron.res
rm cron.res
echo "You should restart the system."
echo "Type: sudo reboot"
reboot