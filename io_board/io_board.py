#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

PiCons - Industrial Process Monitoring System

Copyright (C) [2020] [POLYGONTeam Ltd.]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

# System libraries.
import time
import threading

## GPIO boar control.
# @see http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
import RPi.GPIO as GPIO

## RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip with a RPi.
# @see https://pypi.org/project/mcp3008/
# @see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
from mcp3008 import MCP3008

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "or.dimitrov@polygonteam.com"
"""E-mail of the author.
@see or.dimitrov@polygonteam.com"""

__status__ = "Debug"
"""File status."""

#endregion

class IOBoard():
    """This class is dedicated to drive IO pins of the Rraspberry PI 2/3"""

#region Attributes

    __output_pins = [18, 17, 27, 23]
    """Output pins map. The settings are static because of the IO board."""

    __input_pins = [21, 26, 20, 19, 16, 13]
    """Input pins map. The settings are static because of the IO board."""

    __analog_inputs_map = [8, 9, 10, 11, 12, 13, 14, 15]
    """Analog inputs map."""

    __output_states = [False, False, False, False]
    """Relay output pins states."""

    __input_states = [False, False, False, False, False, False]
    """Digital input pins states."""

    __counters_values = [0, 0, 0, 0, 0, 0]
    """Counters values."""

    __analog_inputs_states = [0, 0, 0, 0, 0, 0, 0, 0]
    """Analog input pin states."""

    __output_len = 0
    """Output pin array len."""

    __input_len = 0
    """Input pin array len."""

    __CLK = 11
    """SPI Clock pin."""

    __MISO = 9
    """SPI MISO pin."""

    __MOSI = 10
    """SPI MOSI pin."""

    __CS = 8
    """SPI CS pis."""

    __adc = None
    """MCP3008 driver instance."""

    __debounce_time = 10
    """Software debounce time. [ms]"""

#endregion

#region Constructor / Destructor

    def __init__(self):
        """Constructor

        Parameters
        ----------
        full_path : str
            Settings file path.

        Returns
        -------
        instance of the class.
            Object
        """

        # Set the board.
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup outputs.
        for pin in self.__output_pins:

            # Initialize pin directions.
            GPIO.setup(pin, GPIO.OUT)

            # Initialize default states.
            GPIO.output(pin, False)

        # Setup inputs.
        for pin in self.__input_pins:

            # Initialize pin directions.
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Initialize the counters.
            self.init_counter(pin)

        # Adafruit_MCP3008.MCP3008(clk=self.__CLK, cs=self.__CS, miso=self.__MISO, mosi=self.__MOSI)
        self.__adc = MCP3008()

        self.__output_len = len(self.__output_pins)
        self.__input_len = len(self.__input_pins)

    def __del__(self):
        """Destructor"""

        # Cleanup he GPIO values.
        GPIO.cleanup()

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

        for index in range(0, len(self.__analog_inputs_map)):

            adc = self.__adc.read([self.__analog_inputs_map[index]])[0]
            self.__analog_inputs_states[index] = IOBoard.from0to10(float(adc))

    def __init_counter(self, index, reset=True):
        """Get the output state.

        Parameters
        ----------
        index : int
            Index of the inputs.

        reset : bool
            Auto reset flag.
        """

        if reset:
            self.set_counter(index)

        GPIO.add_event_detect(\
            self.__input_pins[index], GPIO.FALLING,\
            callback=lambda x: self.__counter_cb(x),\
            bouncetime=self.__debounce_time)
        # GPIO.add_event_detect(bnt, GPIO.RISING,
        # callback=lambda x,y=smp: self.__soundCB(x, y), bouncetime=200)

    def __counter_cb(self, index):
        """Counter callback handler.

        Parameters
        ----------
        index : int
            Index of the input.
        """

        self.__counters_values[index] += 1

    def __pulse_worker(self, index, time_pulse):
        """Thread worker method for timed outputs.

        Parameters
        ----------
        index : int
            Index of the output.

        time_pulse : float
            Seconds to hold the pulse.
        """

        # 1. Switch On the GPIO(index)
        self.set_output(index, True)

        # 2. Wait (time)
        time.sleep(float(time_pulse))

        # 3. Switch Off the GPIO(index)
        self.set_output(index, False)

#endregion

#region Static Methods

    @staticmethod
    def from0to10(value):
        """Scale 0-10 inputs to MCP3008 inputs (3.3V).

        Parameters
        ----------
        index : float
            Voltage value. (0.0 to 3.3)

        Returns
        -------
        Output converted voltage from 0 to 10.
            float
        """

        # Normalize the input value.
        value = value / 1023.0

        # Scale it to 3.3V
        value = value * 3.3

        # voltage devider. [Ohm]
        resistor_r1 = 6800

        # voltage devider. [Ohm]
        resistor_r2 = 3000

        # Math model of the devider.
        result = value * resistor_r2 / (resistor_r1 + resistor_r2)

        # Compensation of the scale. [0V - 10V]
        result = result * 10.928

        return result

#endregion

#region Public Methods

    def get_output(self, index):
        """Get the output state.

        Parameters
        ----------
        index : int
            Index of the output.

        Returns
        -------
        Output state.
            bool
        """

        if index > self.__output_len or index < 0:
            return False

        # Set the state.
        return self.__output_states[index]

    def set_output(self, index, state):
        """Set the output state.

        Parameters
        ----------
        index : int
            Index of the output.

        state : bool
            State of the output.

        Returns
        -------
        Output state.
            bool
        """

        operation = True

        if index > self.__output_len or index < 0:
            operation = False

        # Set the state.
        self.__output_states[index] = state

        # Update output data.
        self.__update_outputs()

        return operation

    def get_outputs(self):
        """Get the outputs states.

        Returns
        -------
        Output states array.
            Array
        """

        return self.__output_states

    def get_input(self, index):
        """Get the input state.

        Parameters
        ----------
        index : int
            Index of the input.

        Returns
        -------
        Input state.
            bool
        """

        if index > self.__input_len or index < 0:
            return False

        # Update input data.
        self.__update_inputs()

        # Return input data.
        return self.__input_states[index]

    def get_inputs(self):
        """Get the inputs state.

        Returns
        -------
        Input states.
            Array
        """

        self.__update_inputs()

        return self.__input_states


    def get_counter(self, index):
        """Get the counter value.

        Parameters
        ----------
        index : int
            Index of the counter.

        Returns
        -------
        Counter value.
            int
        """

        return self.__counters_values[index]

    def set_counter(self, index, value=0):
        """Set the counter value.

        Parameters
        ----------
        index : int
            Index of the counter.

        value : int
            Value for the counter.
        """

        self.__counters_values[index] = value

    def get_counters(self):
        """Returns counters values..

        Returns
        -------
        Counter values.
            Array
        """

        return self.__counters_values

    def pulse(self, index, time_pulse):
        """Generate positive pulse.

        Parameters
        ----------
        index : int
            Index of the output.

        time_pulse : float
            Seconds to hold the pulse.
        """

        if index > 3 or index < 0:
            return

        if time_pulse > 60 or time_pulse < 0:
            return

        process_thread = threading.Thread(\
            target=self.__pulse_worker,\
                args=[index, time_pulse])

        process_thread.start()


    def get_analog(self, index):
        """Get the counter value.

        Parameters
        ----------
        index : int
            Index of the analog input.

        Returns
        -------
        Value of the analog input.
            float
        """

        if index > 7 or index < 0:
            return 0.0

        return self.__analog_inputs_states[index]

    def get_analogs(self):
        """Returns analogs inputs values.

        Returns
        -------
        Analog chanels values. (a0 ... a7)
            Array
        """

        # Return data from ADC.
        return self.__analog_inputs_states

#endregion
