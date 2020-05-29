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

import os
import ConfigParser
import base64

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

class AppSettings():
    """This class is dedicated to hold the application settings."""

#region Attributes

    __full_path = ""
    """Full path to the settings file."""

    __config = None
    """Configuration parser."""

    __enable_write_in_file = False
    """Configuration parser."""

#endregion

#region Constructor / Destructor

    def __init__(self, file_name=None):
        """Constructor

        Parameters
        ----------
        full_path : str
            Settings file path.

        Returns
        -------
        instance of the class.
            Object
        """

        self.__config = ConfigParser.ConfigParser()

        if file_name is None:
            cwd = os.getcwd()
            self.__file_name = os.path.join(cwd, "settings.yaml")

        else:
            self.__file_name = file_name

        if not os.path.exists(self.__file_name):
            self.__create_settings()

        self.__config.read(self.__file_name)

    def __del__(self):
        """Destructor"""

        # Update file.
        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

#endregion

    def __create_settings(self):
        """Create settings file."""

        self.__config.add_section('CREDENTIALS')
        self.__config.set('CREDENTIALS', 'user', 'admin')
        self.__config.set('CREDENTIALS', 'pass', 'admin')
        #self.__config.set('CREDENTIALS', 'server', '127.0.0.1')

        #self.__config.add_section('OUTPUTS')
        #self.__config.set('OUTPUTS', 'Relay1Description', 'Relay 1')
        #self.__config.set('OUTPUTS', 'Relay2Description', 'Relay 2')
        #self.__config.set('OUTPUTS', 'Relay3Description', 'Relay 3')
        #self.__config.set('OUTPUTS', 'Relay4Description', 'Relay 4')

        #self.__config.add_section('INPUTS')
        #self.__config.set('INPUTS', 'DigitalInput1Description', 'Digital1 In1')
        #self.__config.set('INPUTS', 'DigitalInput2Description', 'Digital2 In2')
        #self.__config.set('INPUTS', 'DigitalInput3Description', 'Digital3 In3')
        #self.__config.set('INPUTS', 'DigitalInput4Description', 'Digital4 In4')
        #self.__config.set('INPUTS', 'DigitalInput5Description', 'Digital5 In5')
        #self.__config.set('INPUTS', 'DigitalInput6Description', 'Digital6 In6')

        #self.__config.add_section('ANALOGS')
        #self.__config.set('ANALOGS', 'AnalogInput1Description', 'Analog Inp1')
        #self.__config.set('ANALOGS', 'AnalogInput2Description', 'Analog Inp2')
        #self.__config.set('ANALOGS', 'AnalogInput3Description', 'Analog Inp3')
        #self.__config.set('ANALOGS', 'AnalogInput4Description', 'Analog Inp4')
        #self.__config.set('ANALOGS', 'AnalogInput5Description', 'Analog Inp5')
        #self.__config.set('ANALOGS', 'AnalogInput6Description', 'Analog Inp6')
        #self.__config.set('ANALOGS', 'AnalogInput7Description', 'Analog Inp7')
        #self.__config.set('ANALOGS', 'AnalogInput8Description', 'Analog Inp8')

        self.__config.add_section('COUNTERS')
        #self.__config.set('COUNTERS', 'CounterInput1Description', 'Counter1 In1')
        #self.__config.set('COUNTERS', 'CounterInput2Description', 'Counter2 In2')
        self.__config.set('COUNTERS', 'CounterInput1', '0')
        self.__config.set('COUNTERS', 'CounterInput2', '0')

        self.__config.add_section('DEVICE')
        self.__config.set('DEVICE', 'Name', 'D19')

        # Update file.
        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

        # Read file.
        self.__config.read(self.__full_path)

#region Public Methods

    def update_credentials(self, user, password):
        """Update credentials.

        Parameters
        ----------
        user : str
            Username for this device.

        password : str
            Password for this device.

        """

        if user is not None:
            self.__config.set('CREDENTIALS', 'user', user)

        if user is not None:
            self.__config.set('CREDENTIALS', 'pass', password)

        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    def get_credentials(self):
        """Get credentials

        Returns
        -------
        Array of credentials.
        """

        user = self.__config.get('CREDENTIALS', 'user')
        password = self.__config.get('CREDENTIALS', 'pass')
        return (user, password)

    def get_credentials_as_b64(self):
        """Get credentials as BASE64 encoded directly for HTTP Auth.

        Returns
        -------
        credentials : str
            Returns BASE64 string with the credentials encoded.
        """

        user = self.__config.get('CREDENTIALS', 'user')
        password = self.__config.get('CREDENTIALS', 'pass')
        return base64.b64encode(user + ':' + password)

    def update_counters(self, cnt1, cnt2):
        """Update counters values.

        Parameters
        ----------
        cnt1 : int
            Counter 1 value.

        cnt2 : int
            Counter 2 value.
        """

        if cnt1 > 0:
            # TODO: Fix this shit!
            tmp_cnt1 = self.__config.get('COUNTERS', 'CounterInput1', cnt1)
            self.__config.set('COUNTERS', 'CounterInput1', tmp_cnt1 + cnt1)

        if cnt2 > 0:
            self.__config.set('COUNTERS', 'CounterInput2', cnt2)

        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    def add_counters(self, cnt1, cnt2):
        """Add counters values.

        Parameters
        ----------
        cnt1 : int
            Counter 1 value.

        cnt2 : int
            Counter 2 value.
        """

        if cnt1 > 0:
            tmp_cnt1 = self.__config.get('COUNTERS', 'CounterInput1')
            self.__config.set('COUNTERS', 'CounterInput1', int(tmp_cnt1) + cnt1)

        if cnt2 > 0:
            tmp_cnt2 = self.__config.get('COUNTERS', 'CounterInput2')
            self.__config.set('COUNTERS', 'CounterInput2', int(tmp_cnt2) + cnt2)

        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    def get_counters(self):
        """Returns counters values.

        Returns
        -------
        Counters : array
            Returns arrray of counters values. (cnt1, cnt2)
        """

        cnt1 = self.__config.get('COUNTERS', 'CounterInput1')
        cnt2 = self.__config.get('COUNTERS', 'CounterInput2')
        return (cnt1, cnt2)

    def reset_counters(self, cnt1=0, cnt2=0):
        """Update counters values.

        Parameters
        ----------
        cnt1 : int
            Counter 1 value. It has default value of 0.

        cnt2 : int
            Counter 2 value. It has default value of 0.
        """

        self.__config.set('COUNTERS', 'CounterInput1', cnt1)
        self.__config.set('COUNTERS', 'CounterInput2', cnt2)

        if self.__enable_write_in_file:
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    def get_device_name(self):
        """Returns device name.

        Returns
        -------
        device name : str
            Device name.
        """

        return self.__config.get('DEVICE', 'Name')

#endregion
