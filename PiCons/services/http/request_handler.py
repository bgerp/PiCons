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

from http.server import BaseHTTPRequestHandler

from utils.logger import get_logger
from utils.settings import ApplicationSettings

class RequestHandler(BaseHTTPRequestHandler):
    """Request Handler"""

#region Attributes

    _PROTOCOL_VERSION = "16.11.0.1"
    """Protocol version."""

    _settings = ApplicationSettings.get_instance()
    """Application settingas,"""

    __api_path_evok = "/api/evok-webhooks"
    """API path to EVOK handler."""

    __logger = get_logger(__name__)

#endregion

#region Private Methods

    def _get_mime(self, url_path=""):
        """Returns MIME type.

        Parameters
        ----------
        url_path : str
            URL path.

        Returns
        -------
        str
            MIME type.
        """

        split_string = url_path.split(".")
        extention = ".html"
        mime_type = "text/html"
        split_count = len(split_string)

        if split_count >= 2:

            extention = split_string[split_count - 1]

            if extention == "css":
                mime_type = "text/css"

            elif extention == "jpg":
                mime_type = "image/jpeg"

            elif extention == "jpeg":
                mime_type = "image/jpeg"

            elif extention == "png":
                mime_type = "image/png"

            elif extention == "bmp":
                mime_type = "image/bmp"

            elif extention == "gif":
                mime_type = "image/gif"

            elif extention == "emf":
                mime_type = "image/emf"

            elif extention == "ico":
                mime_type = "image/ico"

            elif extention == "csv":
                mime_type = "text/csv"

            elif extention == "html":
                mime_type = "text/html"

            elif extention == "js":
                mime_type = "text/javascript"

            elif extention == "xml":
                mime_type = "text/xml"

            else:
                mime_type = "text/html"

        return mime_type

#endregion

#region Public Methods

    def do_POST(self):
        """Handler for the POST requests."""

        # The response.
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("OK".encode("utf-8"))

    def do_GET(self):
        """Handler for the GET requests."""

        # Get the key.
        key = self._settings.get_credentials_as_b64

        # Check if it home IP or authorized client respons it.
        if (self.headers["Authorization"] == "Basic " + key)\
             or (self.client_address[0] == "127.0.0.1"):

            mime_type = self._get_mime("*.xml")
            page = self._do_page()

            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Age", "0")
            self.end_headers()
            self.wfile.write(page)

        # Else redirect to authorize.
        elif self.headers["Authorization"] is None:
            self.do_AUTHHEAD()

        # Else redirect to authorize.
        else:
            self.do_AUTHHEAD()

    def do_AUTHHEAD(self):
        """Handler for the authorization."""

        # Set MIME.
        mime_type = self._get_mime()

        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Authorize\"")
        self.send_header("Content-type", mime_type)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Age", "0")
        self.end_headers()
        self.wfile.write("Not authorized.".encode("utf-8"))

#endregion
