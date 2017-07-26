#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''

MIT License

Copyright (c) [2016] [POLYGON Team Ltd.]

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

'''

## Author of the file.
__author__ = "Orlin Dimitrov"

## Copyrighter
#  @see http://polygonteam.com/
__copyright__ = "Copyright 2016, POLYGON Team Ltd."

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

# @see Documentation: https://www.python.org/dev/peps/pep-0008/
# @see Licensing:     http://choosealicense.com/licenses/
# @see Description:   http://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files
# @see Doxygen:       https://www.stack.nl/~dimitri/doxygen/manual/docblocks.html#pythonblocks

import socket, sys, ssl
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from IOServiceHandler import IOServiceHandler

## Server parameters "Default is 8080".
PORT_NUMBER = 80

## Main function of the app.
def main():
    global PORT_NUMBER
    
    # Try to run ...
    try:
        # Create a web server and define the handler
        # to manage the incoming request.
        server = HTTPServer(('', PORT_NUMBER), IOServiceHandler.IOServiceHandler)

        # HTTPS
        # https://gist.github.com/dergachev/7028596
        #server.socket = ssl.wrap_socket(server.socket, certfile='./server.pem', server_side=True)

        # Print network addresses.
        ip_address = socket.gethostbyname(socket.gethostname())
        schema = 'Started server @ {0}:{1}'.format(ip_address, PORT_NUMBER)
        print(schema)

        # Wait forever for incoming http requests.
        server.serve_forever()
        
    except TypeError:
        print('Type error ...')
        
    except KeyboardInterrupt:
        print('^C received, shutting down the server')
        server.socket.close()
        
## Where all begin ...
if(__name__ == '__main__'):
    main()
