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

import json
from http.server import BaseHTTPRequestHandler
from urllib import parse

from services.http.register_handler import RegisterHandler

class RequestHandler(BaseHTTPRequestHandler):
    """Request Handler"""

#region Attributes

    __api_path_evok = "/api/evok-webhooks"
    """API path to EVOK handler."""

#endregion

#region Private Methods

    def __api_evok_webhooks_handler(self):

        # Get content length.
        content_length = self.headers["Content-Length"]
        content_length = int(content_length)

        # Get body request.
        req_body = self.rfile.read(content_length)
        req_body = req_body.decode("utf-8")

        # Convert to JSON object.
        req_body = json.loads(req_body)

        # Update handler.
        RegisterHandler.update(req_body)

        # The response.
        self.send_response(200)
        self.send_header("Content-Type",
                         "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))

#endregion

#region Public Methods

    def do_POST(self):

        parsed_path = parse.urlparse(self.path)

        if parsed_path.path == self.__api_path_evok:
            self.__api_evok_webhooks_handler()

        else:
            # The response.
            self.send_response(200)
            self.send_header("Content-Type",
                            "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("OK".encode("utf-8"))

    def do_GET(self):

        parsed_path = parse.urlparse(self.path)

        if parsed_path.path == self.__api_path_evok:
            self.__api_evok_webhooks_handler()

        else:
            # The response.
            self.send_response(200)
            self.send_header("Content-Type",
                            "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("OK".encode("utf-8"))

#endregion
