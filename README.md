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