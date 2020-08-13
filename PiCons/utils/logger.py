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

from time import gmtime, strftime
import logging

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

#region Variables

__modules_names = []
"""Modules names."""

#endregion

#region Public Functions

def crate_log_file(logs_dir_name="logs/"):
    """This method create a new instance of the LOG direcotry.

    Parameters
    ----------
    logs_dir_name : str
        Path to the log direcotory.
    """

    # Crete log directory.
    if not os.path.exists(logs_dir_name):
        os.makedirs(logs_dir_name)

    # File name.
    log_file = ""
    log_file += logs_dir_name
    log_file += strftime("%Y%m%d", gmtime())
    log_file += ".log"

    # create message format.
    log_format = "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"

    logging.basicConfig( \
        filename=log_file, \
        level=logging.INFO, \
        format=log_format)

def get_logger(module_name):
    """Get logger instance.

    Parameters
    ----------
    module_name : str
        Logger module name.

    Returns
    -------
    logger
        Logger instance.
    """

    global __modules_names

    logger = logging.getLogger(module_name)

    if module_name in __modules_names:
        return logger
    else:
        __modules_names.append(module_name)

    # Create console handler.
    console_handler = logging.StreamHandler()

    # Set debug level.
    console_handler.setLevel(logging.INFO)

    # Add console handler to logger.
    logger.addHandler(console_handler)

    return logger

#endregion
