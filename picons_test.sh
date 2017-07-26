#!/bin/bash
# My first script

echo "Begin ..."
wget -qO- http://127.0.0.1/?Relay1=1
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay1=0
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay2=1
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay2=0
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay3=1
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay3=0
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay4=1
echo ""
sleep 1
wget -qO- http://127.0.0.1/?Relay4=0
echo ""
sleep 1
echo ""
echo "Done ..."