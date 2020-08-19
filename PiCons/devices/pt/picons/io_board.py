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

import time
import threading

# GPIO boar control.
# @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
import RPi.GPIO as GPIO

# RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip with a RPi.
from devices.microchip.mcp3008.mcp3008 import MCP3008

from utils.logger import get_logger


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

class IOBoard():
    """This class is dedicated to drive IO pins of the Raspberry PI 2/3/4."""

    #region Attributes

    __logger = None
    """"Logger"""

    __output_pins = [18, 17, 27, 23]
    """
        Output pins map. The settings are static because of the IO board.
        @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    """

    __input_pins = [21, 26, 20, 19, 16, 13]
    """
        Input pins map. The settings are static because of the IO board.
        @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    """

    __output_states = [False, False, False, False]
    """
        Output pins states.
        @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    """

    __input_states = [False, False, False, False, False, False]
    """
        Input pins states.
        @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
    """

    __analog_inputs_map = [8, 9, 10, 11, 12, 13, 14, 15]
    """Analog inputs map."""

    __output_len = 0
    """Output pin array len."""

    __input_len = 0
    """Input pin array len."""

    __counters_values = [0, 0]
    """Counters values."""

    __adc = None
    """
        MCP3008 driver instance.
        @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
    """

    __debounce_flags = [True, True]
    """Software debounce flags."""

    __debounce_time = 0.04
    """Sotware debounce time."""

    #endregion

    #region Constructor

    def __init__(self):
        """Constructor"""

        self.__logger = get_logger(__name__)

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
        size = len(self.__counters_values)
        for index in range(size):
            self.init_counter(index)

        self.__adc = MCP3008()

        self.__output_len = len(self.__output_pins)
        self.__input_len = len(self.__input_pins)

    def __del__(self):
        """Destructor"""

        # Cleanup he GPIO values.
        GPIO.cleanup()

    #endregion

    #region Public Methods

    def get_output(self, index):
        """Get the output state.

        Parameters
        ----------
        index : int
            Output index.

        Returns
        -------
        bool
            Output state.
        """

        if index > self.__output_len or index < 0:
            return False

        # Set the state.
        return self.__output_states[index]

    def set_output(self, index, state):
        """Get the output state.

        Parameters
        ----------
        index : int
            Output index.
        state : bool
            Output state.

        Returns
        -------
        int
            Operation status.
        """

        if index > self.__output_len or index < 0:
            return False

        # Set the state.
        self.__output_states[index] = state

        # Update output data.
        self.__update_outputs()

        return True

    def get_outputs(self):
        """Get the outputs states.

        Returns
        -------
        []
            Output states array.
        """

        # Update output data.
        self.__update_outputs()

        return self.__output_states

    def get_input(self, index):
        """Get the input state.

        Parameters
        ----------
        index : int
            Input index.

        Returns
        -------
        bool
            Input state.
        """

        if index > self.__input_len or index < 0:
            return False

        # Update input data.
        self.__update_inputs()

        # Return inut data.
        return self.__input_states[index]

    def get_inputs(self):
        """Get the inputs state.

        Returns
        -------
        []
            Input states array.
        """

        # Update input data.
        self.__update_inputs()

        return self.__input_states


    def init_counter(self, index, reset=True):
        """Initialize the counter.

        Parameters
        ----------
        index : int
            Index of the counter.
        reset : bool
            Reset the counter.
        """

        if reset:
            self.reset_counter(index)

        self.__debounce_flags[index] = False
        GPIO.add_event_detect(self.__input_pins[index], GPIO.FALLING, callback=self.__counter_cb)

    def reset_counter(self, index, value=0):
        """Reset counter

        Parameters
        ----------
        index : int
            Index of the counter.
        value : int
            Value of the counter. It has default value of 0.
        """

        self.__counters_values[index] = value

    def get_counter(self, index):
        """Returns counter value.

        Parameters
        ----------
        index : int
            Index of the counter.

        Returns
        -------
        int
            Counter value.
        """
        
        return self.__counters_values[index]

    def get_counters(self):
        """Returns counters values.

        Parameters
        ----------
        index : int
            Index of the counter.

        Returns
        -------
        int
            Counters values.
        """

        return self.__counters_values


    def get_analog(self, index):
        """Returns analog inputs values.

        Parameters
        ----------
        index : int
            Index of the analog input.

        Returns
        -------
        float
            Analog chanel value.
        """

        if(index > 7 or index < 0):
            return 0.0

        value = self.__adc.read([self.__analog_inputs_map[index]])[0]

        value = self.__from0to10(value)
        value = float("{:.3f}".format(value))

        # Return data from ADC.
        return value

    def get_analogs(self):
        """Returns analogs inputs values.

        Returns
        -------
        list
            Analog chanels values. (a0 ... a7)
        """

        # All inputs data.
        adc_values = []

        # Get all inputs.
        for index in range(8):
            adc_values.append(self.get_analog(index))

        # Return data from ADC.
        return adc_values


    def timed_output_set(self, index, pulse_time):
        """Timed set output.

        Parameters
        ----------
        index : int
            Index of the digital input.
        pulse_time : int
            Time to live.
        """

        if(index > 3 or index < 0):
            return

        if(pulse_time > 60 or pulse_time < 0):
            return

        proc_thread = threading.Thread(target=self.__timed_output_set_worker,\
            args=[index, pulse_time])
        proc_thread.start()

    #endregion

    #region Private Methods

    def __update_outputs(self):
        """Update outputs states."""

        for index in range(0, self.__output_len):
            GPIO.output(self.__output_pins[index], self.__output_states[index])

    def __update_inputs(self):
        """Update inputs states."""

        for index in range(0, self.__input_len):
            self.__input_states[index] = GPIO.input(self.__input_pins[index])

    def __clear_debounce(self, index, pulse_time):
        """Clear debounce.

        Parameters
        ----------
        index : int
            Index of the input.
        pulse_time : int
            Time to live.

        Returns
        -------
        int
            Operation status.
        """

        if index < 0 or index > 1:
            return

        time.sleep(pulse_time)
        self.__debounce_flags[index] = True

    def __counter_cb(self, index):
        """Worker thread about counter.

        Parameters
        ----------
        index : int
            Index of the counter.
        """

        if self.__debounce_flags[index]:

            self.__debounce_flags[index] = False
            self.__counters_values[index] += 1
            proc_thread = threading.Thread(target=self.__clear_debounce,\
                args=[index, self.__debounce_time])
            proc_thread.start()

    def __from0to10(self, value):
        """Scale 0-10 inputs to MCP3008 inputs (3.3V).

        Parameters
        ----------
        value : float
            value Voltage value. (0.0 to 3.3)

        Returns
        -------
        float
            Voltage value. (0.0 to 10.0)
        """

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

    def __timed_output_set_worker(self, index, pulse_time):
        """Thread worker method for timed outputs.

        Parameters
        ----------
        index : int
            Index of the analog input.
        pulse_time : int
            Puls time.
        """

        # 1. Swich On the GPIO(index)
        self.set_output(index, True)

        # 2. Wait (time)
        time.sleep(float(pulse_time))

        # 3. Swich Off the GPIO(index)
        self.set_output(index, False)

    #endregion
