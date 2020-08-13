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

class Measurement:
    """This class is dedicated contain units and value."""

    #region Attributes

    __value = None
    """Value of the measurement."""

    __unit = None
    """Unit of the measurement."""

    #endregion

    @property
    def value(self):
        """Value of the measurement."""

        return self.__value

    @property
    def unit(self):
        """Units of the measurement."""

        return self.__unit

    @property
    def is_valid(self):
        """Is valid check procedure."""

        return self.value is not None and self.unit is not None

    #endregion

    #region Constructor

    def __init__(self, value, unit):
        """Constructor

        Parameters
        ----------
        value : float
            value of the measurement.
        unit : str
            Units
        """

        self.__value = value
        self.__unit = unit

    def __str__(self):
        return "Measurement; Value: {}; Unit: {}".format(self.value, self.unit)

    __repr__ = __str__

    #endregion
