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

import os
import time
import configparser
import base64

from utils.logger import get_logger

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

class ApplicationSettings:
    """Settings class organizer."""

#region Attributes

    __logger = None
    """Logger"""

    __instance = None
    """Instance of the class."""

    __file_name = "settings.ini"
    """Full path to the settings file."""

    __config = configparser.ConfigParser()
    """Configuration parser."""

    __enable_write_in_file = False
    """Configuration parser."""

#endregion

#region Properties

    @property
    def exists(self):
        """Does the the settings file exists.

        Returns
        -------
        bool
            File exists.
        """

        return os.path.exists(self.__file_name)

    @property
    def device_name(self):
        """Device name."""

        name = self.__config["DEVICE"]["name"]
        return name

    @property
    def server_port(self):
        """Server port."""

        port = self.__config["SERVER"]["port"]
        port = int(port)
        return port

    @property
    def user(self):
        """User"""

        user = self.__config["CREDENTIALS"]["user"]
        return user

    @property
    def password(self):
        """Pass"""

        password = self.__config["CREDENTIALS"]["pass"]
        return password

    @property
    def get_credentials_as_b64(self):
        """Get credentials as BASE64 encodet directly for HTTP Auth.

        Returns
        -------
        str
            Returns BASE64 string with the credentials encoded.
        """

        user = self.__config["CREDENTIALS"]["user"]
        password = self.__config["CREDENTIALS"]["pass"]
        message = user + ":" + password
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    @property
    def enable_write(self):
        """Enable write in file.

        Returns
        -------
        bool
            enable write in file flag.
        """

        return self.__enable_write_in_file

    @enable_write.setter
    def enable_write(self, value):
        """Enable write in file."""

        self.__enable_write_in_file = value

#endregion

#region Constructor / Destructor

    def __init__(self, file_name=None):
        """Constructor

        Parameters
        ----------
        file_name : str
            File name.
        """

        if file_name is None:
            cwd = os.getcwd()
            self.__file_name = os.path.join(cwd, "settings.ini")

        else:
            self.__file_name = file_name

        # Read setting.
        self.read()

        # Create logger.
        self.__logger = get_logger(__name__)

    def __del__(self):
        """Destructor"""

        self.save()

#endregion

#region Public Methods

    def read(self):
        """Read YAML file."""

        if self.exists:

            self.__config.read(self.__file_name)

    def save(self):
        """Save to file."""

        if self.__enable_write_in_file:

            with open(self.__file_name, "w") as configfile:
                self.__config.write(configfile)

    def create_default(self):
        """Create default settings."""

        if not "SERVER" in self.__config.sections():
            self.__config.add_section("SERVER")
        self.__config.set("SERVER", "port", "8080")

        if not "DEVICE" in self.__config.sections():
            self.__config.add_section("DEVICE")
        self.__config.set("DEVICE", "name", "None")

        if not "CREDENTIALS" in self.__config.sections():
            self.__config.add_section("CREDENTIALS")
        self.__config.set("CREDENTIALS", "user", "admin")
        self.__config.set("CREDENTIALS", "pass", "admin")

        if not "RO" in self.__config.sections():
            self.__config.add_section("RO")
        self.__config.set("RO", "RODescription1", "Relay 1")
        self.__config.set("RO", "RODescription2", "Relay 2")
        self.__config.set("RO", "RODescription3", "Relay 3")
        self.__config.set("RO", "RODescription4", "Relay 4")

        if not "DI" in self.__config.sections():
            self.__config.add_section("DI")
        self.__config.set("DI", "DIDescription1", "Digital In 1")
        self.__config.set("DI", "DIDescription2", "Digital In 2")
        self.__config.set("DI", "DIDescription3", "Digital In 3")
        self.__config.set("DI", "DIDescription4", "Digital In 4")
        self.__config.set("DI", "DIDescription5", "Digital In 5")
        self.__config.set("DI", "DIDescription6", "Digital In 6")

        if not "CI" in self.__config.sections():
            self.__config.add_section("CI")
        self.__config.set("CI", "CIDescription1", "Counter In 1")
        self.__config.set("CI", "CIDescription2", "Counter In 2")
        self.__config.set("CI", "CIValue1", "0")
        self.__config.set("CI", "CIValue2", "0")

        if not "AI" in self.__config.sections():
            self.__config.add_section("AI")
        self.__config.set("AI", "AIDescription1", "Analog In 1")
        self.__config.set("AI", "AIDescription2", "Analog In 2")
        self.__config.set("AI", "AIDescription3", "Analog In 3")
        self.__config.set("AI", "AIDescription4", "Analog In 4")
        self.__config.set("AI", "AIDescription5", "Analog In 5")
        self.__config.set("AI", "AIDescription6", "Analog In 6")
        self.__config.set("AI", "AIDescription7", "Analog In 7")
        self.__config.set("AI", "AIDescription8", "Analog In 8")

        # Save to file.
        self.save()

        # read file.
        self.read()

        self.__logger.warning("New settings file has been created.")

    def update_credentials(self, user, password):
        """Update credentials."""

        if user != None:
            self.__config.set("CREDENTIALS", "user", user)

        if user != None:
            self.__config.set("CREDENTIALS", "pass", password)

        self.save()

    def update_counters(self, cnt1, cnt2):
        """Update counters values."""

        if cnt1 > 0:
            tmp_cnt1 = self.__config.get("CI", "CIValue1", cnt1)
            self.__config.set("CI", "CIValue1", tmp_cnt1 + cnt1)

        if cnt2 > 0:
            self.__config.set("CI", "CIValue2", cnt2)

        self.save()

    def add_counters(self, cnt1, cnt2):
        """Add counters values."""

        if cnt1 > 0:
            tmp_cnt1 = self.__config.get("CI", "CIValue1")
            self.__config.set("CI", "CIValue1", int(tmp_cnt1) + cnt1)

        if cnt2 > 0:
            tmp_cnt2 = self.__config.get("CI", "CIValue2")
            self.__config.set("CI", "CIValue2", int(tmp_cnt2) + cnt2)

        self.save()

    def get_counters(self):
        """Returns counters values."""

        cnt1 = self.__config.get("CI", "CIValue1")
        cnt2 = self.__config.get("CI", "CIValue2")

        return (cnt1, cnt2)

    def reset_counters(self, cnt1=0, cnt2=0):
        """Update counters values."""

        self.__config["CI"]["civalue1"] = cnt1
        self.__config["CI"]["civalue1"] = cnt2

        self.save()

    def ro_name(self, index):
        """Relay outputs name."""

        key = "rodescription" + str(index)
        return self.__config["RO"][key]

    def di_name(self, index):
        """Digitasl input name."""

        key = "didescription" + str(index)
        return self.__config["DI"][key]

    def ci_name(self, index):
        """Counter input name."""

        key = "cidescription" + str(index)
        return self.__config["CI"][key]

    def ai_name(self, index):
        """Analog input name."""

        key = "aidescription" + str(index)
        return self.__config["AI"][key]

#endregion

#region Static Methods

    @staticmethod
    def get_instance(file_path=None):
        """Singelton instance."""

        if ApplicationSettings.__instance is None:
            ApplicationSettings.__instance = ApplicationSettings(file_path)

        return ApplicationSettings.__instance

#endregion
