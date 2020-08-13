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

class Device:
    """Device"""

    #region Attributes

    __name = None
    """Name"""

    __unit = None
    """Units"""

    __id = None
    """Identification"""

    __values = None
    """Values"""

    #endregion

    #region Propertyes

    @property
    def name(self):
        """Name"""

        return self.__name

    @property
    def unit(self):
        """Units"""

        return self.__unit

    @property
    def id(self):
        """Identification"""

        return self.__id

    @property
    def values(self):
        """Values"""

        return self.__values

    @property
    def is_valid(self):
        """Is valid property."""

        return self.name is not None and self.unit is not None and self.id is not None

    @update_values.setter
    def update_values(self, values):
        self.__values = values

    #endregion

    #region constructor

    def __init__(self, name, unit, id):
        """Constructor

        Parameters
        ----------
        name : str
            Name of the device.
        unit : int
            Device unit.
        id : int
            ID
        """

        self.__name = name
        self.__unit = unit
        self.__id = id
        self.__values = []

    def __str__(self):
        return "Device; Name: {}; Unit: {}; ID: {}; Values: {}".format(self.name, self.unit, self.id, self.values)

    __repr__ = __str__

    #endregion
