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

import os
import time
import ConfigParser
import base64

## AppSettings class
#
#  This class is dedicated to drive IO pins of the Rraspberry PI 2/3.
class AppSettings():

    ## Full path to the settings file.
    __full_path = 'settings.ini'
    
    ## Configuration parser.
    __config = ConfigParser.ConfigParser()
    
    ## Configuration parser.
    __enable_write_in_file = False
    
    ## Constructor
    #  @param self The object pointer.
    #  @param full_path This is the path to the settings file. It hase default value the name of the settings file.
    def __init__(self, full_path='settings.ini'):
        # Check the serial port name.
        if(full_path == None):
            raise ValueError('Must enter path.')
        elif(os.path.exists(full_path) == False):
            raise ValueError('Must enter file path.')       
                
        self.__full_path = full_path
        
        self.__config.read(self.__full_path)
        
    ## Destructor
    #  @param self The object pointer.
    def __del__(self):
        # Update file.
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    ## Create default settings.
    #  @param self The object pointer.
    def create_settings(self):
        
        self.__config.add_section('CREDENTIALS')
        self.__config.set('CREDENTIALS', 'user', 'admin')
        self.__config.set('CREDENTIALS', 'pass', 'admin')
        #self.__config.set('CREDENTIALS', 'server', '127.0.0.1')
        
        #self.__config.add_section('OUTPUTS')
        #self.__config.set('OUTPUTS', 'Relay1Description', 'Relay 1')
        #self.__config.set('OUTPUTS', 'Relay2Description', 'Relay 2')
        #self.__config.set('OUTPUTS', 'Relay3Description', 'Relay 3')
        #self.__config.set('OUTPUTS', 'Relay4Description', 'Relay 4')
        
        #self.__config.add_section('INPUTS')
        #self.__config.set('INPUTS', 'DigitalInput1Description', 'Digital In1')
        #self.__config.set('INPUTS', 'DigitalInput2Description', 'Digita2 In2')
        #self.__config.set('INPUTS', 'DigitalInput3Description', 'Digita3 In3')
        #self.__config.set('INPUTS', 'DigitalInput4Description', 'Digita4 In4')
        #self.__config.set('INPUTS', 'DigitalInput5Description', 'Digita5 In5')
        #self.__config.set('INPUTS', 'DigitalInput6Description', 'Digita6 In6')
        
        #self.__config.add_section('ANALOGS')
        #self.__config.set('ANALOGS', 'AnalogInput1Description', 'Analog Inp1')
        #self.__config.set('ANALOGS', 'AnalogInput2Description', 'Analog Inp2')
        #self.__config.set('ANALOGS', 'AnalogInput3Description', 'Analog Inp3')
        #self.__config.set('ANALOGS', 'AnalogInput4Description', 'Analog Inp4')
        #self.__config.set('ANALOGS', 'AnalogInput5Description', 'Analog Inp5')
        #self.__config.set('ANALOGS', 'AnalogInput6Description', 'Analog Inp6')
        #self.__config.set('ANALOGS', 'AnalogInput7Description', 'Analog Inp7')
        #self.__config.set('ANALOGS', 'AnalogInput8Description', 'Analog Inp8')
        
        self.__config.add_section('COUNTERS')
        #self.__config.set('COUNTERS', 'CounterInput1Description', 'Counterl In1')
        #self.__config.set('COUNTERS', 'CounterInput2Description', 'Counterl In2')
        self.__config.set('COUNTERS', 'CounterInput1', '0')
        self.__config.set('COUNTERS', 'CounterInput2', '0')

        self.__config.add_section('DEVICE')
        self.__config.set('DEVICE', 'Name', 'D19')

        # Update file.
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)
        
        # Read file.
        self.__config.read(self.__full_path)
        
    ## Update credentials.
    #  @param self The object pointer.
    #  @param user Username for this device.
    #  @param password Password for this device.
    def update_credentials(self, user, password):

        
        if(user != None):
            self.__config.set('CREDENTIALS', 'user', user)
            
        if(user != None):
            self.__config.set('CREDENTIALS', 'pass', password)
            
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    ## Get credentials
    #  @param self The object pointer.
    #  @return Array of the credentials. (user, pass)
    def get_credentials(self):
        user = self.__config.get('CREDENTIALS', 'user')
        password = self.__config.get('CREDENTIALS', 'pass')
        return (user, password)

    ## Get credentials as BASE64 encodet directly for HTTP Auth.
    #  @param self The object pointer.
    #  @return Returns BASE64 string with the credentials encoded.
    def get_credentials_as_b64(self):
        user = self.__config.get('CREDENTIALS', 'user')
        password = self.__config.get('CREDENTIALS', 'pass')
        return base64.b64encode(user + ':' + password)

    ## Update counters values.
    #  @param self The object pointer.
    #  @param cnt1 Counter 1 value.
    #  @param cnt2 Counter 2 value.
    def update_counters(self, cnt1, cnt2):
        if(cnt1 > 0):
            tmp_cnt1 = self.__config.get('COUNTERS', 'CounterInput1', cnt1)
            self.__config.set('COUNTERS', 'CounterInput1', tmp_cnt1 + cnt1)
            
        if(cnt2 > 0):
            self.__config.set('COUNTERS', 'CounterInput2', cnt2)
            
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)

    ## Add counters values.
    #  @param self The object pointer.
    #  @param cnt1 Counter 1 value.
    #  @param cnt2 Counter 2 value.
    def add_counters(self, cnt1, cnt2):       
        if(cnt1 > 0):
            tmp_cnt1 = self.__config.get('COUNTERS', 'CounterInput1')
            self.__config.set('COUNTERS', 'CounterInput1', int(tmp_cnt1) + cnt1)
            
        if(cnt2 > 0):
            tmp_cnt2 = self.__config.get('COUNTERS', 'CounterInput2')
            self.__config.set('COUNTERS', 'CounterInput2', int(tmp_cnt2) + cnt2)
            
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)
    
    ## Returns counters values.
    #  @param self The object pointer.
    #  @return Returns arrray of counters values. (cnt1, cnt2)
    def get_counters(self):
        cnt1 = self.__config.get('COUNTERS', 'CounterInput1')
        cnt2 = self.__config.get('COUNTERS', 'CounterInput2')
        return (cnt1, cnt2)
    
    ## Update counters values.
    #  @param self The object pointer.
    #  @param cnt1 Counter 1 value. It hase default value of 0.
    #  @param cnt2 Counter 2 value. It hase default value of 0.
    def reset_counters(self, cnt1 = 0, cnt2 = 0):
        self.__config.set('COUNTERS', 'CounterInput1', cnt1)            
        self.__config.set('COUNTERS', 'CounterInput2', cnt2)
            
        if(self.____enable_write_in_file):
            with open(self.__full_path, 'w') as configfile:\
                self.__config.write(configfile)
    
    ## Returns counters values.
    #  @param self The object pointer.
    #  @return Returns device name.
    def get_device_name(self):
        return self.__config.get('DEVICE', 'Name')