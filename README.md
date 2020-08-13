# Pi-Cons WEB based hardware IO controller

The idea of this application is to help WEB based application to talk with industrial hardware.

This application provides simply an HTTP server that generates XML responses.
The content of this responses is state of the digital inputs, digital outputs,
pulsed outputs, analog inputs, electronic scales, etc.

Of course wia HTTP we can manipulate the outputs of the device.

Pi-Cons has LCD display that can displays WEB pages.
This is very useful becaus we can create simple and same time
beautiful user interface with dynamic forms and content.

## Limitations

 - Application is opening only port 80. To change this you should change PORT_NUMBER in main.py.
 - Application can work only with 4 fixed GPIOs as outputs, 6 fixed GPIOs as inputs,
 8 fixed analog inputs via MCP8003. The chip is connected via SPI0.

## Compatible Hardware

The application uses the RAspberry Pi GPIO API for interacting with the
underlying IO hardware. This means it Just Works with a growing number of
boards, including:

 - Raspberry Pi 2 model A
 - Raspberry Pi 2 model B
 - Raspberry Pi 3 model A
 - Raspberry Pi 3 model B

## License

This code is released under the MIT License.
https://opensource.org/licenses/MIT

## Setup the software.
1. Enable SPI:
 - pi@picons:~ $ sudo raspi-config.
 - Use the down arrow to select 5 Interfacing Options
 - Arrow down to P4 SPI.
 - Select yes when it asks you to enable SPI,
 - Also select yes if it asks about automatically loading the kernel module.
 - Use the right arrow to select the <Finish> button.
2. Disable login shell over serial
 - pi@picons:~ $ sudo raspi-config.
 - Use the down arrow to select 5 Interfacing Options
 - Arrow down to P6 Serial.
 - Would you like a login shell to be accessible over │ serial? #No
 - Would you like the serial port hardware to be enabled? #Yes
 - Use the right arrow to select the <Finish> button. 
 - Select yes when it asks to reboot  

3. Go to home directory.

        cd ~

4. Download the software from the repository.

        sudo git clone https://github.com/bgerp/PiCons.git

5. Go to PiCons directory.

        cd PiCons

6. Setup the software.

        sudo bash picons_setup.sh

7. the device will autmaticly reboot affter instalation.

## To make the tests of the device. 

1. Login to the device.

2. Go to home directory.

        cd ~

3. Go to PiCons directory.

        cd PiCons

4. Run the test.

        sudo bash picons_test.sh
