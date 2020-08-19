#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

MIT License

Copyright (c) [2020] [POLYGON Team Ltd.]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import serial

from data.measurement import Measurement

#region File Attributes

## Author of the file.
__author__ = "Orlin Dimitrov"

## Copyrighter
#  @see http://polygonteam.com/
__copyright__ = "Copyright 2020, POLYGON Team Ltd."

## Credits
__credits__ = ["Angel Boyarov"]

## License
#  @see https://opensource.org/licenses/MIT
__license__ = "MIT"

# Version of the file.
__version__ = "1.0.0"

## Name of the author.
__maintainer__ = "Orlin Dimitrov"

## E-mail of the author.
#  @see or.dimitrov@polygonteam.com
__email__ = "or.dimitrov@polygonteam.com"

## File status.
__status__ = "Debug"

#endregion

class VDI3060:
    """This class is dedicated to communicate with electronic scale VDI 30/60."""

    #region Attributes

    __serial_port = None
    """Local serial port.
        @see http://elinux.org/RPi_Serial_Connection"""

    __message_length = 64
    """Message length."""

    __keys_unit = {"kg":"kg", "g":" g", "lb":"lb", "oz":"oz"}
    """Unit keys."""

    __keys_state = {"unstable":"US", "stable":"ST"}
    """State keys."""

    __keys_csv = {"state": 0, "mid": 1, "value": 2}
    """CSV column keys."""

    __min_chunk_len = 2
    """Valid mesage chunk."""

    #endregion

    #region Constructor / Destructor

    def __init__(self, port_name):
        """Constructor

        Parameters
        ----------
        port_name : str
            Serial port name. (/dev/ttyAMA0)
        """

        # Check the serial port name.
        if port_name is None:
            raise ValueError("Must enter serial port name.")

        self.__serial_port = serial.Serial(port_name)

        # Baud rate to 9600.
        self.__serial_port.baudrate = 9600
        # Number of bits per bytes.
        self.__serial_port.bytesize = serial.EIGHTBITS
        # Set parity check: no parity.
        self.__serial_port.parity = serial.PARITY_NONE
        # Number of stop bits.
        self.__serial_port.stopbits = serial.STOPBITS_ONE
        # B read.
        #self.__serial_port.timeout = None
        # Non-b read.
        #self.__serial_port.timeout = 1
        # Timeout b read
        self.__serial_port.timeout = 0.10 # 500 - 20
        # Disable software flow control
        self.__serial_port.xonxoff = False
        # Disable hardware (RTS/CTS) flow control
        self.__serial_port.rtscts = True
        # Disable hardware (DSR/DTR) flow control
        self.__serial_port.dsrdtr = True

    def __del__(self):
        """Destructor"""

        self.disconnect()

    #endregion

    #region Private Methods

    def __parse_data(self, data):
        """Parse data from the serial port.

        Parameters
        ----------
        data : str
            Serial port data.
        """

        # Temporal value.
        measurement = None

        if data is None:
            raise ValueError("Data can not be None.")

        if data == "":
            raise ValueError("Data can not be empty string.")

        # Split data by new line.
        spited_response = data.split("\r\n")

        # If spited array is longer then minimum chunk length proceed.
        if len(spited_response) >= self.__min_chunk_len:

            # Get the second line. Remove new line and split by","(CSV).
            spited_csv = spited_response[self.__min_chunk_len - 1].replace("\r\n", "").split(",")

            if len(spited_csv) != 3:
                raise IndentationError("Invalid package size.", len(spited_csv))

            tmp_key_index = -1
            # Find the matching unit.
            for key_index, key_unit in enumerate(self.__keys_unit):

                # Match the unit.
                if self.__keys_unit[key_unit] in spited_csv[self.__keys_csv["value"]]:

                    # Remove units. Remove white spaces.
                    value = spited_csv[self.__keys_csv["value"]]\
                        .replace(self.__keys_unit[key_unit], "").replace("", "")

                    # Parse to float.
                    value = "{0:.2f}".format(float(value))

                    # Set the temporal value.
                    measurement = Measurement(value, key_unit)

                    # Break if is valid.
                    break

                tmp_key_index = key_index

            if tmp_key_index == len(self.__keys_unit) - 1:
                raise Exception("Invalid unit.", spited_response[self.__min_chunk_len - 1])

                ## If first element is"ST"this means stable.
                #if(splited_csv[self.__keys_csv["state"]] == self.__keys_state["stable"]):
                #    pass
                #else:
                #    raise Exception("Unstable value.", splited_response[self.__min_chunk_len - 1])

        else:
            raise IndexError("Invalid data length.", len(spited_response))


        return measurement

    #endregion

    #region Public Methods

    def connect(self):
        """Connect to device."""

        self.disconnect()
        self.__serial_port.open()

    def disconnect(self):
        """Disconnect from device."""

        if self.__serial_port.isOpen():
            self.__serial_port.close()

    def weight(self):
        """Get the weight of the object on top of the scale."""

        # Response data.
        response = ""

        # Read the response.
        for index in range(self.__message_length):
            response += self.__serial_port.read(1)

        # Return data.
        return self.__parse_data(response)

    #endregion

    #region Public Static Methods

    @staticmethod
    def get_weight(port_name):
        """Get the weight without instancing the class."""

        e_scale = VDI3060(port_name)
        e_scale.connect()
        weight = e_scale.weight()
        del e_scale

        return weight

    #endregion
