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

'''http://user:pass@ip.address/'''

# http://ipaddress/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all

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

import time
import threading
from ElectronicScale import ElectronicScale

## Stop flag.
time_stop = False

def es_worker():
    global time_stop
    
    # Run until time to stop.
    while(not time_stop):
    
        # Try to take mesurment.
        try:
            # Get mesurment.
            mesurment = ElectronicScale.static_get_weight('COM6')
            
            # Print not validated data.            
            if(mesurment.isValid()):
                print mesurment.getValue(), mesurment.getUnit()
            else:
                raise Exception('Invalid mesurment.', mesurment)
                
        # Catch exception.
        except Exception as exception:
            error_text = str(exception.args[0])
            print error_text
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
    
    while(True):
        # Keep alive.
        time.sleep(1)
        print '--- Alive ---'
        pass
    
# Run the program.
if(__name__ == '__main__'):

    # Try to run main().
    try:
        main()
        
    except KeyboardInterrupt:
        time_stop = True
        print('Shutting down the electronic scale.')
