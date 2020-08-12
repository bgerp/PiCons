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

# System libraries.
import time
import threading

## GPIO boar control.
# @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
import RPi.GPIO as GPIO

## RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip with a RPi.
# @see https://pypi.org/project/mcp3008/
import mcp3008

## IOBoard class
#
#  This class is dedicated to drive IO pins of the Rraspberry PI 2/3
class IOBoard():

    ## Output pins map. The settings are static because of the IO board.
    # @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    __output_pins = [18, 17, 27, 23]

    ## Input pins map. The settings are static because of the IO board.
    # @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    __input_pins = [21, 26, 20, 19, 16, 13]
    
    ## Output pins states.
    # @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    __output_states = [False, False, False, False]

    ## Input pins states.
    # @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    __input_states = [False, False, False, False, False, False]

    ## Analog inputs map.
    __analog_inputs_map = [8, 9, 10, 11, 12, 13, 14, 15]
    
    ## Output pin array len.
    __output_len = 0

    ## Input pin array len.
    __input_len = 0

    ## Counters values.
    __counters_values = [0, 0]

    ## SPI Clock pin.
    #  @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    __CLK  = 11

    ## SPI MISO pin.
    #  @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    __MISO = 9

    ## SPI MOSI pin.
    #  @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    __MOSI = 10

    ## SPI CS pis.
    #  @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    __CS   = 8

    ## MCP3008 driver instance.
    #  @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    __adc = None

    ## Software debounce flags.
    __debounce_flags = [True, True]

    ## Sfotware debounce time.
    __debounce_time = 0.04

    ## Constructor
    #  @param self The object pointer.
    def __init__(self):
        
        # Set the board.
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
        # Setup outputs.
        for pin in self.__output_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
            
        # Setup inputs.
        for pin in self.__input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                
        # Initialize the timers.
        self.init_c1()
        self.init_c2()
        
        self.__adc = mcp3008.MCP3008() #Adafruit_MCP3008.MCP3008(clk=self.__CLK, cs=self.__CS, miso=self.__MISO, mosi=self.__MOSI)

        self.__output_len = len(self.__output_pins)
        self.__input_len = len(self.__input_pins)

    ## Destructor
    #  @param self The object pointer.
    def __del__():
        # Cleanup he GPIO values.
        GPIO.cleanup()

    ## Get the output state.
    #  @param self The object pointer.
    #  @param index Index of the output.
    #  @return Output state.
    def get_output(self, index):
        if(index > self.__output_len or index < 0):
            return False
            
        # Set the state.
        return self.__output_states[index]

    ## Set the output state.
    #  @param self The object pointer.
    #  @param index Index of the output.
    #  @param state State of the output.
    def set_output(self, index, state):
        if(index > self.__output_len or index < 0):
            return False
            
        # Set the state.
        self.__output_states[index] = state
        
        # Update output data.
        self.__update_outputs()
    
    ## Get the outputs states.
    #  @param self The object pointer.
    #  @return Output states array.
    def get_outputs(self):
        return self.__output_states
    
    ## Get the input state.
    #  @param self The object pointer.
    #  @param index Index of the input.
    #  @return Input state.
    def get_input(self, index):
        if(index > self.__input_len or index < 0):
            return False
        
        # Update input data.
        self.__update_inputs()
        
        # Return inut data.
        return self.__input_states[index]
        
    ## Get the inputs state.
    #  @param self The object pointer.
    #  @return Input states array.
    def get_inputs(self):
        
        # Update input data.
        self.__update_inputs()
        
        return self.__input_states
    
    ## Update outputs states.
    #  @param self The object pointer.
    def __update_outputs(self):
        for index in range(0, self.__output_len):
            GPIO.output(self.__output_pins[index], self.__output_states[index])

    ## Update inputs states.
    #  @param self The object pointer.
    def __update_inputs(self):
        for index in range(0, self.__input_len):
            self.__input_states[index] = GPIO.input(self.__input_pins[index])

    ## Clear debounce.
    #  @param self The object pointer.
    #  @param index Index of the input.
    #  @param time_to_live Time to live.
    def __clear_debounce(self, index, time_to_live):
        if(index != 0 and index != 1):
            return

        time.sleep(time_to_live)
        self.__debounce_flags[index] = True

    ## Worker thread about counter 0.
    #  @param self The object pointer.
    #  @param index Index of the counter.
    def __worker_c1(self, index):
        if(self.__debounce_flags[0] == True):
            self.__debounce_flags[0] = False
            self.__counters_values[0] += 1
            debounceThread = threading.Thread(target=self.__clear_debounce, args=[0, self.__debounce_time])
            debounceThread.start()

    ## Worker thread about counter 1.
    #  @param self The object pointer.
    #  @param index Index of the counter.
    def __worker_c2(self, index):
        if(self.__debounce_flags[1] == True):
            self.__debounce_flags[1] = False
            self.__counters_values[1] += 1
            debounceThread = threading.Thread(target=self.__clear_debounce, args=[1, self.__debounce_time])
            debounceThread.start()

    ## Reset counter 0.
    #  @param self The object pointer.
    #  @param value Value of the counter. It has default value of 0.
    def reset_counter1(self, value = 0):
        self.__counters_values[0] = value

    ## Reset counter 1.
    #  @param self The object pointer.
    #  @param value Value of the counter. It has default value of 0.
    def reset_counter2(self, value = 0):
        self.__counters_values[1] = value

    ## Initialize the counter 0.
    #  @param self The object pointer.
    #  @param reset Reset the counter.
    def init_c1(self, reset = True):
        if(reset):
            self.reset_counter1()
            
        self.__soft_debounce_1 = False
        GPIO.add_event_detect(self.__input_pins[0], GPIO.FALLING, callback=self.__worker_c1)

    ## Initialize counter 1.
    #  @param self The object pointer.
    #  @param reset Reset the counter.
    def init_c2(self, reset=True):
        if(reset):
            self.reset_counter2()
            
        self.__soft_debounce_2 = False
        GPIO.add_event_detect(self.__input_pins[1], GPIO.FALLING, callback=self.__worker_c2)

    ## Retuens counter 1 value.
    #  @param self The object pointer.
    #  @return Counter 1 value.
    def get_counter1(self):
        return self.__counters_values[0]

    ## Retuens counter 2 value.
    #  @param self The object pointer.
    #  @return Counter 2 value.
    def get_counter2(self):
        return self.__counters_values[1]

    ## Retuens counters values.
    #  @param self The object pointer.
    #  @return Counters values. (c1, c2)
    def get_counters(self):
        return self.__counters_values

    ## Retuens analog inputs values.
    #  @param self The object pointer.
    #  @param index Index of the analog input.
    #  @return Analog chanel value.
    def get_analog(self, index):
        if(index > 7 or index < 0):
            return 0.0
            
        # Return data from ADC.
        adc = self.__adc.read([self.__analog_inputs_map[index]])[0]
        values[i] = self.__from0to10(float(adc))
        return values[i]

    ## Retuens analogs inputs values.
    #  @param self The object pointer.
    #  @return Analog chanels values. (a0 ... a7)
    def get_analogs(self):
        values = [0]*8
        
        for index in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            adc = self.__adc.read([self.__analog_inputs_map[index]])[0]
            values[index] = self.__from0to10(float(adc))
        
        # Return data from ADC.
        return values

    ## Scale 0-10 inputs to MCP3008 inputs (3.3V).
    #  @param self The object pointer.
    #  @param value Voltage value. (0.0 to 3.3)
    #  @return Voltage value. (0.0 to 10.0)
    def __from0to10(self, value):
        # Normalize the input value.
        value = value / 1023.0
        # Scale it to 3.3V
        value = value * 3.3
        R1 = 6800 # voltage devider. [Ohm]
        R2 = 3000 # voltage devider. [Ohm]
        # Math model of the devider.
        result = value * R2 / (R1 + R2)
        # Compensation of the scale. [0V - 10V]
        result = result * 10.928
        return result
    
    ## Timed set output.
    #  @param index Index of the analog input.
    #  @param time_to_live Time to live.
    def timed_output_set(self, index, time_to_live):
        if(index > 3 or index < 0):
            return
    
        if(time_to_live > 60 or time_to_live < 0):
            return
            
        processThread = threading.Thread(target=self.__timed_output_set_worker, args=[index, time_to_live])
        processThread.start();
    
    ## Thread worker method for timed outputs.
    #  @param index Index of the analog input.
    #  @param time_to_live Time to live.
    def __timed_output_set_worker(self, index, time_to_live):
        # 1. Swich On the GPIO(index)
        self.set_output(index, True)
        # 2. Wait (time)
        time.sleep(float(time_to_live))
        # 3. Swich Off the GPIO(index)
        self.set_output(index, False)
        
