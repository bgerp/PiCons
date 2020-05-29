#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

PiCons - Industrial Process Monitoring System

Copyright (C) [2020] [POLYGONTeam Ltd.]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import serial
from measurement import Measurement

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "or.dimitrov@polygonteam.com"
"""E-mail of the author.
@see or.dimitrov@polygonteam.com"""

__status__ = "Debug"
"""File status."""

#endregion

class ElectronicScale():
    """This class is dedicated to communicate with electronic scale."""

#region Attributes

    # @see http://elinux.org/RPi_Serial_Connection
    __serial_port = serial.Serial()
    """Local serial port"""

    __message_length = 64
    """Message length."""

    __keys_unit = {"kg": "kg", "g": "g", "lb": "lb", "oz": "oz"}
    """Unit keys."""

    __keys_state = {"unstable": "US", "stable": "ST"}
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
            Serial port name.

        Returns
        -------
        instance of the class.
            Object
        """

        # Check the serial port name.
        if port_name is None or port_name == "":
            raise ValueError("Must enter serial port name.")

        # Port name.
        self.__serial_port.port = port_name

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
            Incoming data from the scale.
        """

        # Temporal value.
        measurement = None

        # If data is somethind proceed.
        if data is not None:

            # Split data by new line.
            splitted_response = data.split("\r\n")

            # If splitted array is longer then minimum chunk length proceed.
            if len(splitted_response) >= self.__min_chunk_len:

                # Get the second line. Remove new line and split by "," (CSV).
                splitted_csv = splitted_response[self.__min_chunk_len - 1]\
                    .replace("\r\n", "").split(",")

                if len(splitted_csv) != 3:
                    raise Exception("Invalid package size.", len(splitted_csv))

                tmp_key_index = -1
                # Find the matching unit.
                for key_index, key_unit in enumerate(self.__keys_unit):

                    # Match the unit.
                    if self.__keys_unit[key_unit] in splitted_csv[self.__keys_csv["value"]]:

                        # Remove units. Remove white spaces.
                        value = splitted_csv[self.__keys_csv["value"]]\
                            .replace(self.__keys_unit[key_unit], "").replace(" ", "")

                        # Parse to float.
                        value = "{0:.2f}".format(float(value))

                        # Set the temporal value.
                        measurement = Measurement(value, key_unit)

                        # Break if is valid.
                        break

                    tmp_key_index = key_index

                if tmp_key_index == len(self.__keys_unit) - 1:
                    raise Exception("Invalid unit.", splitted_response[self.__min_chunk_len - 1])

                ## If first element is "ST" this means stable.
                #if(splitted_csv[self.__keys_csv["state"]] == self.__keys_state["stable"]):
                #    pass
                #else:
                #    raise Exception("Unstable value.", splitted_response[self.__min_chunk_len - 1])

            else:
                raise Exception("Invalid data length.", len(splitted_response))

        else:
            raise Exception("No data.", data)

        return measurement

#endregion

#region Public Methods

    def connect(self):
        """Connect to the scale."""

        self.disconnect()
        self.__serial_port.open()

    def disconnect(self):
        """Disconnect"""

        if self.__serial_port.isOpen():
            self.__serial_port.close()

    def get_weight(self):
        """Get weight from the measurement."""

        # Response data.
        response = ""

        # Read the response.
        for byte in range(self.__message_length):
            response += self.__serial_port.read(1)

        # Return data.
        return self.__parse_data(response)

#endregion

#region Static Methods

    @staticmethod
    def static_get_weight(port_name):
        """Get the weight without instancing the class.

        Parameters
        ----------
        port_name : str
            Serial port name.
        """

        e_scale = ElectronicScale(port_name)
        e_scale.connect()
        weight = e_scale.get_weight()
        e_scale.disconnect()
        del e_scale

        return weight

#endregion
