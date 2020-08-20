#!/bin/bash

echo "Begin ..."
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080/?Relay1=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay1=0"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay2=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay2=0"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay3=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay3=0"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay4=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?Relay4=0"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080/?ToggleRelay1=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?ToggleRelay2=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?ToggleRelay3=1"
sleep 1
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?ToggleRelay4=1"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080/?PulseRelay1=2"
sleep 5
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?PulseRelay2=2"
sleep 5
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?PulseRelay3=2"
sleep 5
echo ""
echo ""
wget -q -O - "http://127.0.1.1:8080/?PulseRelay4=2"
sleep 5
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?RelayOutputs=all"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?Relay1=1&Relay2=1&Relay3=1&Relay4=1"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?Relay1=0&Relay2=0&Relay3=0&Relay4=0"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?DigitalInputs=all"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?CounterInputs=all"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?AnalogInputs=all"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080?ElectronicScales=all"
sleep 1
echo ""
echo ""

# =============================================================================
wget -q -O - "http://127.0.1.1:8080/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all"
sleep 1
echo ""
echo ""

# =============================================================================
echo "Done ..."
