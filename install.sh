#!/bin/bash

FILE=/var/log/firstboot
#Check if booting for first time
if [ ! -f "$FILE" ]; then
  SERIAL_NUMBER=$(python3 /opt/PiCons/info.py -s)
  #clear the minion config
  cat /dev/null >/etc/salt/minion

  echo "  master: 109.199.153.86" >>/etc/salt/minion

  echo "  id: sn$SERIAL_NUMBER" >>/etc/salt/minion

  systemctl restart salt-minion
  bash /opt/Zontromat/sh/generate_settings.sh
  #Set timezone
  timedatectl set-timezone Europe/Sofia

  #set hostname
  /opt/unipi/tools/unipihostname

  #Make sure it would not run again
  touch /var/log/firstboot
fi
