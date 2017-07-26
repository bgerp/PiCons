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
import threading
import serial
import Measurement

## ElectronicScale class
#
#  This class is dedicated to communicate with electronic scale.
class ElectronicScale():

    ## Local serial port
    #  @see http://elinux.org/RPi_Serial_Connection
    __serial_port = serial.Serial()
    
    ## Message length.
    __message_length = 64
    
    ## Unit keys.
    __keys_unit = { 'kg' : 'kg' , 'g' : ' g' , 'lb' : 'lb' , 'oz' : 'oz' }
    
    ## State keys.
    __keys_state = { 'unstable' : 'US' , 'stable' : 'ST'}
    
    ## CSV column keys.
    __keys_csv = { 'state' : 0, 'mid' : 1, 'value' : 2 }
    
    ## Valid mesage chunk.
    __min_chunk_len = 2
    
    ## Constructor
    #  @param self The object pointer.
    #  @param port_name Serial port name. (/dev/ttyAMA0)
    def __init__(self, port_name):
        # Check the serial port name.
        if(port_name == None):
            raise ValueError('Must enter serial port name.')
        else:
            self.__serial_port.port = port_name
            
        # Baud rate to 9600.
        self.__serial_port.baudrate = 9600
        # Number of bits per bytes.
        self.__serial_port.bytesize = serial.EIGHTBITS
        # Set parity check: no parity.
        self.__serial_port.parity = serial.PARITY_NONE
        # Number of stop bits.
        self.__serial_port.stopbits = serial.STOPBITS_ONE 
        # B read.
        #self.__serial_port.timeout = None
        # Non-b read.
        #self.__serial_port.timeout = 1
        # Timeout b read
        self.__serial_port.timeout = 0.10 # 500 - 20
        # Disable software flow control
        self.__serial_port.xonxoff = False
        # Disable hardware (RTS/CTS) flow control
        self.__serial_port.rtscts = True
        # Disable hardware (DSR/DTR) flow control
        self.__serial_port.dsrdtr = True
    
    ## Destructor
    #  @param self The object pointer.
    def __del__(self):
        self.dissconnect()
    
    ## Parse data from the serial port.
    #  @param self The object pointer.
    #  @param data Serial port data.
    def __parse_data(self, data):
                
        # Temporal value.
        measurement = None

        # If data is somethind proceed.
        if(data is not ''):
        
            if(data is None):
                raise Exception('Invalid data.', data)
                
            # Split data by new line.
            splited_response = data.split('\r\n')
                        
            # If splited array is longer then minimum chunk length proceed.
            if(len(splited_response) >= self.__min_chunk_len):
                
                # Get the second line. Remove new line and split by ',' (CSV).
                splited_csv = splited_response[self.__min_chunk_len - 1].replace('\r\n', '').split(',')
                
                if(len(splited_csv) != 3):
                    raise Exception('Invalid package size.', len(splited_csv))
                   
                tmp_key_index = -1
                # Find the matching unit.
                for key_index, key_unit in enumerate(self.__keys_unit):
                    
                    # Match the unit.
                    if(self.__keys_unit[key_unit] in splited_csv[self.__keys_csv['value']]):
                
                        # Remove units. Remove white spaces.
                        value = splited_csv[self.__keys_csv['value']].replace(self.__keys_unit[key_unit], '').replace(' ', '')
                        
                        # Parse to float.
                        value = "{0:.2f}".format(float(value))
                        
                        # Set the temporal value.
                        measurement = Measurement.Measurement(value, key_unit)
                                                    
                        # Break if is valid.
                        break
                    
                    tmp_key_index = key_index
                    
                if(tmp_key_index == len(self.__keys_unit) - 1):
                    raise Exception('Invalid unit.', splited_response[self.__min_chunk_len - 1])
                
                ## If first element is 'ST' this means stable.
                #if(splited_csv[self.__keys_csv['state']] == self.__keys_state['stable']):
                #    pass
                #else:
                #    raise Exception('Unstable value.', splited_response[self.__min_chunk_len - 1])
                    
            else:
                raise Exception('Invalid data length.', len(splited_response))
                
        else:
            raise Exception('No data.', data)
            
        return measurement
    
    ## Connect to device.
    #  @param self The object pointer.
    def connect(self):
        self.dissconnect()            
        self.__serial_port.open()
    
    ## Disconnect from device.
    #  @param self The object pointer.
    def dissconnect(self):
        if(self.__serial_port.isOpen()):
            self.__serial_port.close()
    
    ## Get the weight of the objec on top of the scale.
    #  @param self The object pointer.
    def get_weight(self):
        
        # Response data.
        response = ''        
        
        # Read the response.
        for bytes in range(self.__message_length):
            response += self.__serial_port.read(1)
            
        # Return data.
        return self.__parse_data(response)
    
    ## Get the weight without instancing the class.
    #  @param port_name Serial port name. (/dev/ttyAMA0)
    @staticmethod
    def static_get_weight(port_name):
        e_scale = ElectronicScale(port_name)
        e_scale.connect()
        weight = e_scale.get_weight()
        e_scale.dissconnect()
        return weight
    