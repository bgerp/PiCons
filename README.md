# Pi-Cons WEB based hardware IO controller

The idea of this application is to help WEB based application to talk with industrial hardwar.

This application provides simply an HTTP server that ggenerates XML responses.
The content of this responses is state of the digital inputs, digital outpust,
pulsed outputs, analog inputs, electronic scales, etc.

Ofcourse wia HTTP we can manipulate the outputs of the device.

Pi-Cons has LCD display that can displays WEB pages.
This is verry usefull becaus we can create simple and same time
beautifull user interface with dynamic forms and content.

## Limitations

 - Application is opening only port 80. To change this you shoud change PORT_NUMBER in main.py.
 - Application can work only with 4 fixet GPIOs as outputs, 6 fixet GPIOs as inputs,
 8 fixet analog inputs via MCP8003. The chip is connected via SPI0.

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

1. Go to home directory.

        cd ~

2. Download the software from the repository.

        sudo git clone https://git@github.com/bgerp/PiCons.git

3. Go to PiCons directory.

        cd PiCons

4. Setup the software.

        sudo bash picons_setup.sh

5. the device will autmaticly reboot affter instalation.

## To make the tests of the device. 

1. Login to the device.

2. Go to home directory.

        cd ~

3. Go to PiCons directory.

        cd PiCons

4. Run the test.

        sudo bash picons_test.sh