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


"""http://user:pass@ip.address/"""

# http://ipaddress/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all

import os, time, socket, sys, urllib, platform, base64
import collections
from uuid import getnode as get_mac
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from uuid import getnode as get_mac

import xml.etree.ElementTree as ET

# https://pypi.python.org/pypi/dicttoxml
import dicttoxml

from IOBoard import IOBoard
from ElectronicScale import ElectronicScale
from ElectronicScale import Measurement
from AppSettings import AppSettings
from IOUtils import IOUtils
from KioskSettings import KioskSettings

## IOServiceHandler class
#
#  This class will handles any incoming request from the clients.
class IOServiceHandler(BaseHTTPRequestHandler):
    
    ## IO board abstracion driver.
    __board = IOBoard.IOBoard()
    
    ## Application settings.
    __settings = AppSettings.AppSettings("/home/pi/PiCons/settings.ini")
    
    ## KIOSK browser settings.
    __kioskSettings = KioskSettings.KioskSettings("/home/pi/.config/autostart/autoChromium.desktop")
    
    ## Page body.
    __the_page = "OK"
        
    ## MIME type of the response.
    __mime_type = ""
    
    ## Relay 1 command key. Value: 1 or 0
    __RELAY_1 = "Relay1" 
    ## Relay 2 command key. Value: 1 or 0
    __RELAY_2 = "Relay2"
    ## Relay 3 command key. Value: 1 or 0
    __RELAY_3 = "Relay3"
    ## Relay 4 command key. Value: 1 or 0
    __RELAY_4 = "Relay4"
    
    ## Toggle relay 1 command key. Value: 1
    __TOGGLE_RELAY_1 = "ToggleRelay1"
    ## Toggle relay 2 command key. Value: 1
    __TOGGLE_RELAY_2 = "ToggleRelay2"
    ## Toggle relay 3 command key. Value: 1
    __TOGGLE_RELAY_3 = "ToggleRelay3"
    ## Toggle relay 4 command key. Value: 1
    __TOGGLE_RELAY_4 = "ToggleRelay4"
    
    ## Pulse relay 4 command key. Value: 1 to 60[s]
    __PULSE_RELAY_1 = "PulseRelay1"
    ## Pulse relay 4 command key. Value: 1 to 60[s]
    __PULSE_RELAY_2 = "PulseRelay2"
    ## Pulse relay 4 command key. Value: 1 to 60[s]
    __PULSE_RELAY_3 = "PulseRelay3"
    ## Pulse relay 4 command key. Value: 1 to 60[s]
    __PULSE_RELAY_4 = "PulseRelay4"
    
    ## Address of the KIOSK browser in BASE64.
    __KIOSK_ADDRESS = "KioskAddress"
    ## Preset the default settings of the browser.
    __KIOSK_DEFAULT = "KioskDefault"
    
    ## Relay outputs descriptor. 
    __RO  = {"key" : "RelayOutputs",    "name" : "RelayOutput",     "unit" : "LogicLevel", "id" : {"1": "0", "2": "1", "3": "2", "4": "3"}}
    ## Digital inputs descriptor.                                   
    __DI = {"key" : "DigitalInputs",    "name" : "DigitalInput",    "unit" : "LogicLevel", "id" : {"1": "4", "2": "5", "3": "6", "4": "7", "5": "8", "6": "9"}}
    ## Counters inputs descriptor.                                  
    __CI = {"key" : "CounterInputs",    "name" : "CounterInput",    "unit" : "Count",      "id" : {"1": "10", "2": "11"}}
    ## Analog inputs descriptor.                                    
    __AI = {"key" : "AnalogInputs",     "name" : "AnalogInput",     "unit" : "V",          "id" : {"1": "12", "2": "13", "3": "14", "4": "15", "5": "16", "6": "17", "7": "18", "8": "19"}}
    ## Electronic scales descriptor.
    __ES = {"key" : "ElectronicScales", "name" : "ElectronicScale",                        "id" : {"1": "20"}}
    
    ## Protocol version.
    __PROTOCOL_VERSION = "16.11.0.1"

    ## Text representation of logic level 0.
    __STATE_LOW = "0"
    ## Text representation of logic level 1.
    __STATE_HIGH = "1"

    ## Get the key.
    
    ## Handler for the GET requests.
    #  @param self The object pointer.
    def do_GET(self):

        # Get the key.
        key = self.__settings.get_credentials_as_b64()
        
        # Check if it home IP or authorized client respons it.
        if (self.headers.getheader("Authorization") == "Basic " + key) or (self.client_address[0] == "127.0.0.1"):
            # Just pass and proseed.
            pass

        # Else redirect to authorize.
        elif (self.headers.getheader("Authorization") == None):
            self.do_AUTHHEAD()
            self.wfile.write("no auth header received")
            pass

        # Else redirect to authorize.
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader("Authorization"))
            self.wfile.write("not authenticated")
            pass

        # Parse the URL path.
        parsed_url = urlparse(self.path)
        
        # Check is there arguments.
        if(parsed_url.query != None and parsed_url.query != ""):
            # Create the response.
            self.__the_page = self.__create_get_response(parsed_url.query)
        else:
            # Create XML structure.
            container = dict()
            container["ProtocolVersion"] = self.__PROTOCOL_VERSION
            container["Entrys"] = None
            
            xml = dicttoxml.dicttoxml(container, custom_root="Monitor", attr_type=False)
            # Create the response.
            self.__the_page = xml
            
        # ============================================

        self.send_response(200)
        self.send_header("Content-type", self.__mime_type)
        self.send_header("Access-Control-Allow-Origin", "*") # This may be usefull as a settings. Only the central server can call the IO device.
        #self.send_header("Access-Control-Allow-Methods", "GET") # This may be usefull only with get method to access the device.
        self.end_headers()
        # Send the page
        self.wfile.write(self.__the_page)
        
        return

        
    ## Handler for the authorization.
    #  @param self The object pointer.
    def do_AUTHHEAD(self):
        # Set MIME.
        self.__mime_type = "text/xml"
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Test\"")
        self.send_header("Content-type", self.__mime_type)
        self.end_headers()
        
    ## Translate relative path to absolute.
    #  @param self The object pointer.
    #  @param url_path relative path from the request.
    def __from_realative_to_absolute(self, url_path):
        
        curent_path = os.path.dirname(os.path.realpath(__file__))
        full_path = curent_path + url_path
        if(os.name == "nt"):
            full_path = full_path.replace("/", "\\")
        
        if(os.path.isdir(full_path) == True):
            full_path = os.path.join(full_path, self.__default_file_name)
        elif(os.path.isfile(full_path) == True):
            full_path = full_path
            
        return full_path

    ## Get the content from the file.
    #  @param self The object pointer.
    #  @param file_path file path that wil get the content.
    def __get_content(self, file_path):
        content = ""
        # Open the file.
        page_file = open(file_path, "rb")
        # Read page file content.
        content = page_file.read()
        # Close the content.
        page_file.close()
        
        return content
        
    ## Returns MIME type.
    #  @param self The object pointer.
    #  @param url_path URL path.
    def __get_mime(self, url_path):
        split_string = url_path.split(".")
        extention = ""
        mime_type = ""
        split_count = len(split_string)
        if(split_count >= 2):
            extention = split_string[split_count - 1]
            if(extention == "css"):
                mime_type = "text/css"
            elif(extention == "jpg"):
                mime_type = "image/jpeg"
            elif(extention == "jpeg"):
                mime_type = "image/jpeg"
            elif(extention == "png"):
                mime_type = "image/png"
            elif(extention == "bmp"):
                mime_type = "image/bmp"
            elif(extention == "gif"):
                mime_type = "image/gif"
            elif(extention == "emf"):
                mime_type = "image/emf"
            elif(extention == "ico"):
                mime_type = "image/ico"
            elif(extention == "csv"):
                mime_type = "text/csv"
            elif(extention == "html"):
                mime_type = "text/html"
            elif(extention == "js"):
                mime_type = "text/javascript"
            elif(extention == "xml"):
                mime_type = "text/xml"
            else:
                mime_type = "text/html"
            
        return mime_type
    
    ## Generate entry.
    #  @param self The object pointer.
    #  @param units Units of the mesurment in the entry.
    #  @param id ID of the entry.
    #  @param name Name of the entry.
    #  @param value Value of the mesurment.
    def __generate_entry(self, units, id, name, value):
        entry = dict()
        
        entry["Unit"] = units
        entry["ID"] = id
        entry["Name"] = name
        entry["Value"] = value
        
        return entry
    
    ## Create XML response.
    #  @param self The object pointer.
    #  @param url_query URL path.
    def __create_get_response(self, url_query):
        
        query_dict = dict()
        
        # Entrys container list.
        entries = []
        
        if(url_query != None):
            #query = urllib.unquote(url_query).decode("utf8")
            ucq_dict = parse_qs(url_query)
            query_dict = dict([(str(key), str(value[0])) for key, value in ucq_dict.items()])
        
        # If relay 1 is in the arguments prse it.
        if(self.__RELAY_1 in query_dict):
            state = query_dict[self.__RELAY_1]
            if(state == "0"):
                self.__board.set_output(0, False)
            if(state == "1"):
                self.__board.set_output(0, True)
                
        # If relay 2 is in the arguments prse it.
        if(self.__RELAY_2 in query_dict):
            state = query_dict[self.__RELAY_2]
            if(state == "0"):
                self.__board.set_output(1, False)
            if(state == "1"):
                self.__board.set_output(1, True)
                
        # If relay 3 is in the arguments prse it.
        if(self.__RELAY_3 in query_dict):
            state = query_dict[self.__RELAY_3]
            if(state == "0"):
                self.__board.set_output(2, False)
            if(state == "1"):
                self.__board.set_output(2, True)
                
        # If relay 4 is in the arguments prse it.
        if(self.__RELAY_4 in query_dict):
            state = query_dict[self.__RELAY_4]
            if(state == "0"):
                self.__board.set_output(3, False)
            if(state == "1"):
                self.__board.set_output(3, True)
                
        # If toggle relay 1 is in the arguments prse it.
        if(self.__TOGGLE_RELAY_1 in query_dict):
            state = str(query_dict[self.__TOGGLE_RELAY_1][0])
            if(state == "1"):
                state = not self.__board.get_output(0)
                self.__board.set_output(0, state)
                
        # If toggle relay 2 is in the arguments prse it.
        if(self.__TOGGLE_RELAY_2 in query_dict):
            state = query_dict[self.__TOGGLE_RELAY_2]
            if(state == "1"):
                state = not self.__board.get_output(1)
                self.__board.set_output(1, state)
                
        # If toggle relay 3 is in the arguments prse it.
        if(self.__TOGGLE_RELAY_3 in query_dict):
            state = query_dict[self.__TOGGLE_RELAY_3]
            if(state == "1"):
                state = not self.__board.get_output(2)
                self.__board.set_output(2, state)
                
        # If toggle relay 4 is in the arguments prse it.
        if(self.__TOGGLE_RELAY_4 in query_dict):
            state = query_dict[self.__TOGGLE_RELAY_4]
            if(state == "1"):
                state = not self.__board.get_output(3)
                self.__board.set_output(3, state)
                
        # If pulse relay 1 is in the arguments prse it.
        if(self.__PULSE_RELAY_1 in query_dict):
            sTime = query_dict[self.__PULSE_RELAY_1]
            try:
                fTime = float(sTime)
                self.__board.timed_output_set(0, fTime)
            except:
                pass
                
        # If pulse relay 2 is in the arguments prse it.
        if(self.__PULSE_RELAY_2 in query_dict):
            sTime = query_dict[self.__PULSE_RELAY_2]
            try:
                fTime = float(sTime)
                self.__board.timed_output_set(1, fTime)
            except:
                pass
                
        # If pulse relay 3 is in the arguments prse it.
        if(self.__PULSE_RELAY_3 in query_dict):
            sTime = query_dict[self.__PULSE_RELAY_3]
            try:
                fTime = float(sTime)
                self.__board.timed_output_set(2, fTime)
            except:
                pass
                
        # If pulse relay 4 is in the arguments prse it.
        if(self.__PULSE_RELAY_4 in query_dict):
            sTime = query_dict[self.__PULSE_RELAY_4]
            try:
                fTime = float(sTime)
                self.__board.timed_output_set(3, fTime)
            except:
                pass
                
        # If kiosk browser address is in the arguments prse it.
        if(self.__KIOSK_ADDRESS in query_dict):
            b64address = query_dict[self.__KIOSK_ADDRESS]
            try:
                address = base64.b64decode(str(b64address))
                self.__kioskSettings.update_address(address)
            except e:
                print e
                pass
                
        # If kiosk browser default settings is in the arguments prse it.
        if(self.__KIOSK_DEFAULT in query_dict):
            value = query_dict[self.__KIOSK_DEFAULT]
            try:
                self.__kioskSettings.create_default_settings()
            except e:
                print e
                pass
                        
        # Check if the relay outputs key is in the list.
        if(self.__RO["key"] in query_dict):
        
            indexes = query_dict[self.__RO["key"]]
            
            relay_outputs = self.__board.get_outputs()
            
            # If the key is all then get all relay outputs.
            if(indexes == "all"):
                for index in range(len(self.__RO["id"])):
                
                    # Get ID of the entry item.
                    id = self.__RO["id"][str(index + 1)]

                    # Get value of the entry item.
                    value = self.__STATE_HIGH if relay_outputs[index] else self.__STATE_LOW
                    
                    # Create nama of the entry item.
                    name = self.__RO["name"] + str(index + 1)
                    
                    # Generate entry item.
                    entry = self.__generate_entry(self.__RO["unit"], id, name, value)
                    
                    # Add entry item to entries.
                    entries.append(entry)
                
            # If the key is array.
            elif(indexes <> ""):

                # Split by coma.
                indexes_splited = indexes.split(",")

                # Remove dublicates and sort.
                indexes_splited = sorted(list(set(indexes_splited)))

                # If the length is grater then one.
                for index in range(len(indexes_splited)):
                    if(indexes_splited[index] in self.__RO["id"]):
                        
                        # Get ID of the entry item.
                        id = self.__RO["id"][indexes_splited[index]]

                        # Get value of the entry item.
                        value = self.__STATE_HIGH if relay_outputs[index] else self.__STATE_LOW
                        
                        # Create name of the entry item.
                        name = self.__RO["name"] + indexes_splited[index]
                        
                        # Generate entry item.
                        entry = self.__generate_entry(self.__RO["unit"], id, name, value)
                        
                        # Add entry item to entries.
                        entries.append(entry)

        # Check if the digital inputs key is in the list.
        if(self.__DI["key"] in query_dict):
        
            # Get content from the arguments.
            indexes = query_dict[self.__DI["key"]]
            
            # Read inputs.
            digital_inputs = self.__board.get_inputs()
            
            # If the key is all then get all relay inputs.
            if(indexes == "all"):
                for index in range(len(self.__DI["id"])):
                    
                    # Get ID of the entry item.
                    id = self.__DI["id"][str(index + 1)]
                        
                    # Get value of the entry item.
                    value = self.__STATE_HIGH if digital_inputs[index] else self.__STATE_LOW
                    
                    # Create nama of the entry item.
                    name = self.__DI["name"] + str(index + 1)
                    
                    # Generate entry item.
                    entry = self.__generate_entry(self.__DI["unit"], id, name, value)
                    
                    # Add entry item to entries.
                    entries.append(entry)
                
            # If the key is array.
            elif(indexes <> ""):

                # Split by coma.
                indexes_splited = indexes.split(",")

                # Remove dublicates and sort.
                indexes_splited = sorted(list(set(indexes_splited)))


                # If the length is grater then one.
                for index in range(len(indexes_splited)):
                    if(indexes_splited[index] in self.__DI["id"]):
                    
                        # Get ID of the entry item.
                        id = self.__DI["id"][indexes_splited[index]]
                    
                        # Get value of the entry item.
                        value = self.__STATE_HIGH if digital_inputs[index] else self.__STATE_LOW
                        
                        # Create nama of the entry item.
                        name = self.__DI["name"] + indexes_splited[index]
                        
                        # Generate entry item.
                        entry = self.__generate_entry(self.__DI["unit"], id, name, value)
                        
                        # Add entry item to entries.
                        entries.append(entry)
                        
        # Check if the counter inputs key is in the list.
        if(self.__CI["key"] in query_dict):
        
            # Get content from the arguments.
            indexes = query_dict[self.__CI["key"]]
            
            # Read counters_inputs.
            cnt_get1 = self.__board.get_counter1()
            cnt_get2 = self.__board.get_counter2()
            self.__settings.add_counters(cnt_get1, cnt_get2)
            self.__board.reset_counter1()
            self.__board.reset_counter2()
            (cnt_get1, cnt_get2) = self.__settings.get_counters()
            counters_inputs = (cnt_get1, cnt_get2)
            
            # If the key is all then get all counters_inputs.
            if(indexes == "all"):
                for index in range(len(self.__CI["id"])):
                    
                    # Get ID of the entry item.
                    id = self.__CI["id"][str(index + 1)]
                
                    # Get value of the entry item.
                    value = counters_inputs[index]
                    
                    # Create name of the entry item.
                    name = self.__CI["name"] + str(index + 1)
                    
                    # Generate entry item.
                    entry = self.__generate_entry(self.__CI["unit"], id, name, value)
                    
                    # Add entry item to entries.
                    entries.append(entry)
                
            # If the key is array.
            elif(indexes <> ""):

                # Split by coma.
                indexes_splited = indexes.split(",")

                # Remove dublicates and sort.
                indexes_splited = sorted(list(set(indexes_splited)))

                # If the length is grater then one.
                for index in range(len(indexes_splited)):
                    if(indexes_splited[index] in self.__CI["id"]):
                    
                        # Get ID of the entry item.
                        id = self.__CI["id"][indexes_splited[index]]
                    
                        # Get value of the entry item.
                        value = counters_inputs[index]
                        
                        # Create name of the entry item.
                        name = self.__CI["name"] + indexes_splited[index]
                        
                        # Generate entry item.
                        entry = self.__generate_entry(self.__CI["unit"], id, name, value)
                        
                        # Add entry item to entries.
                        entries.append(entry)
                 
        # Check if the analog inputs key is in the list.
        if(self.__AI["key"] in query_dict):
        
            # Get content from the arguments.
            indexes = query_dict[self.__AI["key"]]
            
            # Read analog alaog inputs.
            alaog_inputs = self.__board.get_analogs()
            
            # If the key is all then get all relay alaog inputs.
            if(indexes == "all"):
                for index in range(len(self.__AI["id"])):
                    
                    # Get ID of the entry item.
                    id = self.__AI["id"][str(index + 1)]
                    
                    # Get value of the entry item.
                    value = alaog_inputs[index]
                    
                    # Create nama of the entry item.
                    name = self.__AI["name"] + str(index + 1)
                    
                    # Generate entry item.
                    entry = self.__generate_entry(self.__AI["unit"], id, name, value)
                    
                    # Add entry item to entries.
                    entries.append(entry)
                
            # If the key is array.
            elif(indexes <> ""):

                # Split by coma.
                indexes_splited = indexes.split(",")

                # Remove dublicates.
                indexes_splited = list(set(indexes_splited))

                # If the length is grater then one.
                for index in range(len(indexes_splited)):
                    if(indexes_splited[index] in self.__AI["id"]):
                    
                        # Get ID of the entry item.
                        id = self.__AI["id"][indexes_splited[index]]
                    
                        # Get value of the entry item.
                        value = alaog_inputs[index]
                        
                        # Create nama of the entry item.
                        name = self.__AI["name"] + str(index + 1)
                        
                        # Generate entry item.
                        entry = self.__generate_entry(self.__AI["unit"], id, name, value)
                        
                        # Add entry item to entries.
                        entries.append(entry)

        # Check if the electronic scale key is in the list.
        if(self.__ES["key"] in query_dict):
        
            # Get content from the arguments.
            indexes = query_dict[self.__ES["key"]]
            
            mesurment = None
            
            # Read the electronic scale.
            try:
                mesurment = ElectronicScale.ElectronicScale.static_get_weight("/dev/serial0") # "/dev/serial0"
                
            # Catch exception.
            except Exception as exception:
                error_text = str(exception.args[0])
                mesurment = ElectronicScale.Measurement.Measurement(error_text, "")
                
                print "Electronic scale exception: " + error_text
                # TODO: Log the error for a week.
                #print type(exception)     # the exception instance
                #print exception.args[0]      # arguments stored in .args
                #print exception           # __str__ allows args to be printed directly
                pass

            # Data container.
            es_inputs = []
            es_inputs.append(mesurment)
            
            # If the key is all then get all electronic scales.
            if(indexes == "all"):
                for index in range(len(self.__ES["id"])):
                                        
                    # Get ID of the entry item.
                    id = self.__ES["id"][str(index + 1)]
                        
                    # Create nama of the entry item.
                    name = self.__ES["name"] + str(index + 1)
                    
                    # Tmporal fields.
                    value = ""
                    unit = ""
                    
                    # Get value of the entry item.
                    if(es_inputs[index] != None):
                        if(es_inputs[index].isValid()):
                            value = es_inputs[index].getValue()
                            unit = es_inputs[index].getUnit()
                    
                    # Generate entry item.
                    es_entry = self.__generate_entry(unit, id, name, value)
                    
                    # Add entry item to entries.
                    entries.append(es_entry)
                
            # If the key is array.
            elif(indexes <> ""):

                # Split by coma.
                indexes_splited = indexes.split(",")

                # Remove dublicates and sort.
                indexes_splited = sorted(list(set(indexes_splited)))

                # If the length is grater then one.
                for index in range(len(indexes_splited)):
                    if(indexes_splited[index] in self.__ES["id"]):
                    
                        # Get ID of the entry item.
                        id = self.__ES["id"][indexes_splited[index]]
                        
                        # Create nama of the entry item.
                        name = self.__ES["name"] + indexes_splited[index]
                        
                        # Tmporal fields.
                        value = ""
                        unit = ""
                        
                        # Get value of the entry item.
                        if(es_inputs[index] != None and es_inputs[index].isValid()):
                            value = es_inputs[index].getValue()
                            unit = es_inputs[index].getUnit()
                                                    
                        # Generate entry item.
                        es_entry = self.__generate_entry(unit, id, name, value)
                        
                        # Add entry item to entries.
                        entries.append(es_entry)

        # Create XML structure.
        device = dict()
        device["Entries"] = entries
        device["Name"] = key = self.__settings.get_device_name()
        
        devices = []
        devices.append(device)
        
        container = dict()
        container["Devices"] = devices
        container["ProtocolVersion"] = self.__PROTOCOL_VERSION
                
        xml = dicttoxml.dicttoxml(container, custom_root="Monitor", attr_type=False)
        
        return xml
        
