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

# http://user:pass@ipaddress/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all

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

class Measurement():
    """This class is dedicated contain units and value."""

#region Attributes

    __value = None
    """Value"""

    __unit = None
    """Unit"""

#endregion

#region Constructor

    def __init__(self, value, unit):
        """Constructor

        Parameters
        ----------
        value : float
            Value of the measurement.

        unit : str
            Units of the measurement.

        Returns
        -------
        instance of the class.
            Object
        """

        self.__value = value
        self.__unit = unit

    def __str__(self):

        return "Value: {}; Unit: {}".format(self.value, self.unit)

    __repr__ = __str__

#endregion

#region Properties

    @property
    def value(self):
        """Value

        Returns
        -------
        value : float
            Value of the measurement.
        """

        return self.__value

    @property
    def unit(self):
        """Unit

        Returns
        -------
        value : str
            Unit of the measurement.
        """

        return self.__unit

    @property
    def is_valid(self):
        """Is valid flag

        Returns
        -------
        value : bool
            If the both field are set.
        """

        return self.__value is not None and self.__unit is not None

#endregion
