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

import socket
import signal

from utils.logger import get_logger, crate_log_file

from services.http.server import Server

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

__server = None
"""Server"""

__time_to_stop = False
"""Stop flag."""

__logger = None
"""Logger"""

def interupt_handler(signum, frame):
    """Interupt handler."""

    global __server, __time_to_stop

    __time_to_stop = True

    if signum == 2:
        print("Stopped by interupt.")

    elif signum == 15:
        print("Stopped by termination.")

    else:
        print("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    __server.stop()
    __time_to_stop = True

def main():
    """Main function."""

    global __server, __time_to_stop

    # Create log.
    crate_log_file()
    __logger = get_logger(__name__)

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    ip_address = socket.gethostbyname(socket.gethostname())
    __server = Server(ip_address, 8080)
    __server.start()

    print("Starting server, use <Ctrl-C> to stop")

    while not __time_to_stop:
        pass

if __name__ == "__main__":
    main()