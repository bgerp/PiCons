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

import ConfigParser

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

class KioskSettings:
    """This class is dedicated to control the chromium browser."""

    ## Full path to the settings file.
    __full_path = ""
    
    ## Configuration parser.
    __config = ConfigParser.ConfigParser()
    
    ## Command that invoke Chromium WEB browser in KIOSK mod.
    __cb_command = "/usr/bin/chromium-browser --noerrdialogs --disable-session-crashed-bubble --disable-infobars --kiosk "
    
    ## Desktop entry that describe the fields.
    __desktop_entry = "Desktop Entry"
    
    # ~/.config/autostart/autoChromium.desktop
    """
    [Desktop Entry]
    Type=Application
    Exec=/usr/bin/chromium-browser --noerrdialogs --disable-session-crashed-bubble --disable-infobars --kiosk http://server2
    Hidden=false
    X-GNOME-Autostart-enabled=true
    Name[en_US]=AutoChromium
    Name=AutoChromium
    Comment=Start Chromium when GNOME starts
    """

    ## Constructor
    #  @param self The object pointer.
    #  @param full_path Full path to the settings file.
    def __init__(self, full_path = ""):
        # Check the serial port name.
        if(full_path == None):
            raise ValueError("Must enter path.")
        elif(os.path.exists(full_path) == False):
            raise ValueError("Must enter file path.")
                
        self.__full_path = full_path
        
        # To save the file with kays.
        self.__config.optionxform = str
                 
    ## Destructor
    #  @param self The object pointer.
    def __del__(self):
        pass

    ## Create default settings.
    #  @param self The object pointer.
    def create_default_settings(self):
        self.__config.add_section(self.__desktop_entry)
        self.__config.set(self.__desktop_entry, "Type", "Application")
        self.__config.set(self.__desktop_entry, "Exec", self.__cb_command + "http://polygonteam.com")
        self.__config.set(self.__desktop_entry, "Hidden", "false")
        self.__config.set(self.__desktop_entry, "X-GNOME-Autostart-enabled", "true")
        self.__config.set(self.__desktop_entry, "Name[en_US]", "AutoChromium")
        self.__config.set(self.__desktop_entry, "Name", "AutoChromium")
        self.__config.set(self.__desktop_entry, "Comment", "Start Chromium when GNOME starts")

        with open(self.__full_path, "w") as configfile:\
            self.__config.write(configfile)

    ## Update browser address.
    #  @param self The object pointer.
    #  @param address Address of the page.
    def update_address(self, address):
    
        self.__config.read(self.__full_path)
    
        self.__config.set(self.__desktop_entry, "Exec", self.__cb_command + address)
        
        with open(self.__full_path, "w") as configfile:\
            self.__config.write(configfile)

        # 1. Check if the browser is runing.
        # 2. If yes kill the browser.
        # 3. Run run new instance of the browser.
        # self.__cb_command + address
        print "Restarting ..."
    
    ## Stop kiosk browser.
    #  @param self The object pointer.
    def stop_browser(self):
        print "stop_browser"
