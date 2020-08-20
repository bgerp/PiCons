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

import signal
import socket
import time

from utils.logger import get_logger, crate_log_file
from utils.settings import AppSettings
from utils.utils import get_local_ip

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

#region Variables

__server = None
"""Server"""

__time_to_stop = False
"""Stop flag."""

__logger = None
"""Logger"""

#endregion

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

    __setting = AppSettings.get_instance()
    while not __setting.exists:
        __logger.info("Settings not exists.")
        __setting.enable_write = True
        __setting.create_default()
        __setting.enable_write = False
        time.sleep(1)

    __logger.info("Application started for device: {}".format(__setting.device_name))

    # Add signal handler.
    signal.signal(signal.SIGINT, interupt_handler)
    signal.signal(signal.SIGTERM, interupt_handler)

    # Run the WEB service.
    # ip_address = get_local_ip()
    # ip_address = socket.gethostbyname(socket.gethostname())
    # __server = Server(ip_address, __setting.server_port)
    __server = Server("", __setting.server_port)
    __server.start()

    # Hold the runtime.
    print("Starting server, use <Ctrl-C> to stop")
    while not __time_to_stop:
        pass

if __name__ == "__main__":
    main()
