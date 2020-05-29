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

# http://user:pass@ipaddress/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all

import time
import threading
from electronic_scale.electronic_scale import ElectronicScale

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

## Stop flag.
time_stop = False

def es_worker():
    global time_stop

    # Run until time to stop.
    while not time_stop:

        # Try to take measurement.
        try:
            # Get measurement.
            measurement = ElectronicScale.static_get_weight("COM6")

            # Print not validated data.
            if measurement.is_valid:
                print(measurement)

            else:
                raise Exception("Invalid measurement.", measurement)

        # Catch exception.
        except Exception as exception:
            error_text = str(exception.args[0])
            print(error_text)
            # TODO: Log the error for a week.
            #print type(exception)     # the exception instance
            #print exception.args[0]      # arguments stored in .args
            #print exception           # __str__ allows args to be printed directly
            pass

        time.sleep(0.03)

# Main function.
def main():
    # Create the thread.
    es_thread = threading.Thread(target=es_worker)
    es_thread.start()

    while True:
        # Keep alive.
        time.sleep(1)
        print("--- Alive ---")

# Run the program.
if __name__ == "__main__":

    # Try to run main().
    try:
        main()

    except KeyboardInterrupt:
        time_stop = True
        print("Shutting down the electronic scale.")
