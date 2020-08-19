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

from threading import Thread 

from http.server import HTTPServer

from services.http.io_handler import IOHandler

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

class Server:

#region Attributes

    __logger = None
    """Logger"""

    __host = "127.0.0.1"
    """Host"""

    __port = 8889
    """Port"""

    __server = None
    """WEB server."""

    __thread = None
    """Thread"""

#endregion

#region Constructor

    def __init__(self, host="127.0.0.1", port=8889):

        if host is not None:
            self.__host = host

        if port is not None:
            self.__port = port

        # Create logger.
        self.__logger = get_logger(__name__)

#endregion

#region Properties

    @property
    def is_alive(self):

        state = False

        if self.__thread is not None:
            state = self.__thread.is_alive()

        return state

#endregion

#region Private Methods

    def __worker(self, args):
        self.__server.serve_forever()

#endregion

#region Public Methods

    def start(self):
        # Create two threads as follows
        try:
            if self.__thread is None:

                # Create
                self.__thread = Thread(target=self.__worker, args=(33,))
                self.__server = HTTPServer((self.__host, self.__port), IOHandler)

                # Start if not.
                if not self.__thread.is_alive():
                    self.__thread.start()

                    self.__logger.info("Start WEB service.")

        except Exception as e:
            self.__logger.error(e)

    def stop(self):

        try:
            if self.__thread is not None:

                # If it is alive join.
                if self.__thread.is_alive():

                    # Shutdown the server.
                    self.__server.shutdown()

                    # Wait to stop.
                    while self.__thread.is_alive():
                        pass

                    self.__thread.join()

                    # Delete
                    self.__thread = None
                    self.__server = None

                    self.__logger.info("Stop WEB service.")

        except Exception as e:
            self.__logger.error(e)

#endregion
