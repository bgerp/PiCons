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

from urllib import parse
# from urlparse import urlparse, parse_qs

import dicttoxml

from services.http.request_handler import RequestHandler

from devices.pt.picons.io_board import IOBoard
from devices.vedicom.vdi3060.vdi3060 import VDI3060

from data.measurement import Measurement

# wget -q -O - "http://admin:admin@127.0.1.1:8080/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all"
# wget -q -O - "http://127.0.1.1:8080/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all"
# wget -q -O - "http://127.0.1.1:8080?"

# wget -q -O - "http://127.0.1.1:8080?RelayOutputs=all"
# wget -q -O - "http://127.0.1.1:8080?Relay1=1&Relay2=1&Relay3=1&Relay4=1"
# wget -q -O - "http://127.0.1.1:8080?Relay1=0&Relay2=0&Relay3=0&Relay4=0"

# wget -q -O - "http://127.0.1.1:8080?DigitalInputs=all"

# wget -q -O - "http://127.0.1.1:8080?CounterInputs=all"

# wget -q -O - "http://127.0.1.1:8080?AnalogInputs=all"

# wget -q -O - "http://127.0.1.1:8080?ElectronicScales=all"


class IOHandler(RequestHandler):
    """Request Handler"""

#region Attributes

    __RELAY_1 = "Relay1"
    """Relay 1 command key. Value: 1 or 0"""

    __RELAY_2 = "Relay2"
    """Relay 2 command key. Value: 1 or 0"""

    __RELAY_3 = "Relay3"
    """Relay 3 command key. Value: 1 or 0"""

    __RELAY_4 = "Relay4"
    """Relay 4 command key. Value: 1 or 0"""

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

    __io_board = IOBoard()
    """IO board."""

    __entries = []
    """Entries"""

#endregion

#region Protected Methods

    def _do_page(self):

        # Clear the entries.
        self.__entries.clear()

        # Clear the body.
        page_body = ""

        # Parse the URL path.
        parsed_url = parse.urlparse(self.path)

        # Check is there arguments.
        if self.__is_empty_query(parsed_url.query):

            ucq_dict = parse.parse_qs(parsed_url.query)
            query_dict = dict([(str(key), str(value[0])) for key, value in ucq_dict.items()])

            self.__do_ro(query_dict)
            self.__do_di(query_dict)
            self.__do_ci(query_dict)
            self.__do_ai(query_dict)
            self.__do_es(query_dict)

        # Create XML structure.
        container = dict()
        container["ProtocolVersion"] = self._PROTOCOL_VERSION
        container["Device"] = self._settings.device_name
        container["Entrys"] = self.__entries

        page_body = dicttoxml.dicttoxml(container, custom_root="Monitor", attr_type=False)

        # print(page_body.decode("ascii"))

        return page_body

#endregion

#region Private Methods

    def __is_empty_query(self, query):
        """Is empty query.

        Parameters
        ----------
        query : str
            Query object.

        Returns
        -------
        bool
            Is empty or not.
        """

        return query != None and query != ""

    def __generate_entry(self, units, id, name, value):
        """Generate entry.

        Parameters
        ----------
        units : str
            Units of the measurement in the entry.
        id : int
            ID of the entry.
        name : str
            Name of the entry.
        value : mix
            Value of the measurement.

        Returns
        -------
        dict
            The entry.
        """

        entry = dict()

        entry["Unit"] = units
        entry["ID"] = id
        entry["Name"] = name
        entry["Value"] = value

        return entry

    def __do_ro(self, query_dict):

        # If relay 1 is in the arguments parse it.
        if self.__RELAY_1 in query_dict:
            state = query_dict[self.__RELAY_1]
            if state == "0":
                self.__io_board.set_output(0, False)
            if state == "1":
                self.__io_board.set_output(0, True)

        # If relay 2 is in the arguments parse it.
        if self.__RELAY_2 in query_dict:
            state = query_dict[self.__RELAY_2]
            if state == "0":
                self.__io_board.set_output(1, False)
            if state == "1":
                self.__io_board.set_output(1, True)

        # If relay 3 is in the arguments parse it.
        if self.__RELAY_3 in query_dict:
            state = query_dict[self.__RELAY_3]
            if state == "0":
                self.__io_board.set_output(2, False)
            if state == "1":
                self.__io_board.set_output(2, True)

        # If relay 4 is in the arguments parse it.
        if self.__RELAY_4 in query_dict:
            state = query_dict[self.__RELAY_4]
            if state == "0":
                self.__io_board.set_output(3, False)
            if state == "1":
                self.__io_board.set_output(3, True)

        # If toggle relay 1 is in the arguments parse it.
        if self.__TOGGLE_RELAY_1 in query_dict:
            state = str(query_dict[self.__TOGGLE_RELAY_1][0])
            if state == "1":
                state = not self.__io_board.get_output(0)
                self.__io_board.set_output(0, state)

        # If toggle relay 2 is in the arguments parse it.
        if self.__TOGGLE_RELAY_2 in query_dict:
            state = query_dict[self.__TOGGLE_RELAY_2]
            if state == "1":
                state = not self.__io_board.get_output(1)
                self.__io_board.set_output(1, state)

        # If toggle relay 3 is in the arguments parse it.
        if self.__TOGGLE_RELAY_3 in query_dict:
            state = query_dict[self.__TOGGLE_RELAY_3]
            if state == "1":
                state = not self.__io_board.get_output(2)
                self.__io_board.set_output(2, state)

        # If toggle relay 4 is in the arguments parse it.
        if self.__TOGGLE_RELAY_4 in query_dict:
            state = query_dict[self.__TOGGLE_RELAY_4]
            if state == "1":
                state = not self.__io_board.get_output(3)
                self.__io_board.set_output(3, state)

        # If pulse relay 1 is in the arguments parse it.
        if self.__PULSE_RELAY_1 in query_dict:
            str_time = query_dict[self.__PULSE_RELAY_1]
            try:
                flt_time = float(str_time)
                self.__io_board.timed_output_set(0, flt_time)
            except:
                pass

        # If pulse relay 2 is in the arguments parse it.
        if self.__PULSE_RELAY_2 in query_dict:
            str_time = query_dict[self.__PULSE_RELAY_2]
            try:
                flt_time = float(str_time)
                self.__io_board.timed_output_set(1, flt_time)
            except:
                pass

        # If pulse relay 3 is in the arguments parse it.
        if self.__PULSE_RELAY_3 in query_dict:
            str_time = query_dict[self.__PULSE_RELAY_3]
            try:
                flt_time = float(str_time)
                self.__io_board.timed_output_set(2, flt_time)
            except:
                pass

        # If pulse relay 4 is in the arguments parse it.
        if self.__PULSE_RELAY_4 in query_dict:
            str_time = query_dict[self.__PULSE_RELAY_4]
            try:
                flt_time = float(str_time)
                self.__io_board.timed_output_set(3, flt_time)
            except:
                pass

        # Check if the relay outputs key is in the list.
        if self.__RO["key"] in query_dict:

            indexes = query_dict[self.__RO["key"]]

            relay_outputs = self.__io_board.get_outputs()

            # If the key is all then get all relay outputs.
            if indexes == "all":

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
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_spited = indexes.split(",")

                # Remove duplicates and sort.
                indexes_spited = sorted(list(set(indexes_spited)))

                # If the length is grater then one.
                for index in range(len(indexes_spited)):

                    if indexes_spited[index] in self.__RO["id"]:

                        # Get ID of the entry item.
                        id = self.__RO["id"][indexes_spited[index]]

                        # Get value of the entry item.
                        value = self.__STATE_HIGH if relay_outputs[index] else self.__STATE_LOW

                        # Create name of the entry item.
                        name = self.__RO["name"] + indexes_spited[index]

                        # Generate entry item.
                        entry = self.__generate_entry(self.__RO["unit"], id, name, value)

                        # Add entry item to entries.
                        self.__entries.append(entry)

    def __do_di(self, query_dict):

        # Check if the digital inputs key is in the list.
        if self.__DI["key"] in query_dict:

            # Get content from the arguments.
            indexes = query_dict[self.__DI["key"]]

            # Read inputs.
            digital_inputs = self.__io_board.get_inputs()

            # If the key is all then get all relay inputs.
            if indexes == "all":

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
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove dublicates and sort.
                indexes_split = sorted(list(set(indexes_split)))


                # If the length is grater then one.
                for index in range(len(indexes_split)):
                    if indexes_split[index] in self.__DI["id"]:

                        # Get ID of the entry item.
                        id = self.__DI["id"][indexes_split[index]]

                        # Get value of the entry item.
                        value = self.__STATE_HIGH if digital_inputs[index] else self.__STATE_LOW

                        # Create nama of the entry item.
                        name = self.__DI["name"] + indexes_split[index]

                        # Generate entry item.
                        entry = self.__generate_entry(self.__DI["unit"], id, name, value)

                        # Add entry item to entries.
                        self.__entries.append(entry)

    def __do_ci(self, query_dict):

        # Check if the counter inputs key is in the list.
        if self.__CI["key"] in query_dict:

            # Get content from the arguments.
            indexes = query_dict[self.__CI["key"]]

            # Read counters_inputs.
            cnt_0 = self.__io_board.get_counter(0)
            cnt_1 = self.__io_board.get_counter(1)

            # Save counters.
            self._settings.add_counters(cnt_0, cnt_1)

            # Reset counters.
            self.__io_board.reset_counter(0)
            self.__io_board.reset_counter(1)

            # Get counters from settings.
            (cnt_0, cnt_1) = self._settings.get_counters()

            # Apply
            counters_inputs = (cnt_0, cnt_1)

            # If the key is all then get all counters_inputs.
            if indexes == "all":

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
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates and sort.
                indexes_split = sorted(list(set(indexes_split)))

                # If the length is grater then one.
                for index in range(len(indexes_split)):

                    if indexes_split[index] in self.__CI["id"]:

                        # Get ID of the entry item.
                        id = self.__CI["id"][indexes_split[index]]

                        # Get value of the entry item.
                        value = counters_inputs[index]

                        # Create name of the entry item.
                        name = self.__CI["name"] + indexes_split[index]

                        # Generate entry item.
                        entry = self.__generate_entry(self.__CI["unit"], id, name, value)

                        # Add entry item to entries.
                        self.__entries.append(entry)

    def __do_ai(self, query_dict):

        # Check if the analog inputs key is in the list.
        if self.__AI["key"] in query_dict:

            # Get content from the arguments.
            indexes = query_dict[self.__AI["key"]]

            # Read analog inputs.
            analog_inputs = self.__io_board.get_analogs()

            # If the key is all then get all relay analog inputs.
            if indexes == "all":
                for index in range(len(self.__AI["id"])):

                    # Get ID of the entry item.
                    id = self.__AI["id"][str(index + 1)]

                    # Get value of the entry item.
                    value = analog_inputs[index]

                    # Create nama of the entry item.
                    name = self.__AI["name"] + str(index + 1)

                    # Generate entry item.
                    entry = self.__generate_entry(self.__AI["unit"], id, name, value)

                    # Add entry item to entries.
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates.
                indexes_split = list(set(indexes_split))

                # If the length is grater then one.
                for index in range(len(indexes_split)):
                    if indexes_split[index] in self.__AI["id"]:

                        # Get ID of the entry item.
                        id = self.__AI["id"][indexes_split[index]]

                        # Get value of the entry item.
                        value = analog_inputs[index]

                        # Create nama of the entry item.
                        name = self.__AI["name"] + str(index + 1)

                        # Generate entry item.
                        entry = self.__generate_entry(self.__AI["unit"], id, name, value)

                        # Add entry item to entries.
                        self.__entries.append(entry)

    def __do_es(self, query_dict):
        # Check if the electronic scale key is in the list.
        if self.__ES["key"] in query_dict:

            # Get content from the arguments.
            indexes = query_dict[self.__ES["key"]]

            measurement = None

            # Read the electronic scale.
            try:
                measurement = VDI3060.get_weight("/dev/serial0") # "/dev/serial0"

            # Catch exception.
            except Exception as exception:
                error_text = str(exception.args[0])
                measurement = Measurement(error_text, "")

                print("Electronic scale exception: {}".format(error_text))
                # TODO: Log the error for a week.
                #print type(exception)     # the exception instance
                #print exception.args[0]      # arguments stored in .args
                #print exception           # __str__ allows args to be printed directly
                pass

            # Data container.
            es_inputs = []
            es_inputs.append(measurement)

            # If the key is all then get all electronic scales.
            if indexes == "all":
                for index in range(len(self.__ES["id"])):

                    # Get ID of the entry item.
                    id = self.__ES["id"][str(index + 1)]

                    # Create nama of the entry item.
                    name = self.__ES["name"] + str(index + 1)

                    # Temporal fields.
                    value = ""
                    unit = ""

                    # Get value of the entry item.
                    if es_inputs[index] != None:
                        if es_inputs[index].is_valid:
                            value = es_inputs[index].value
                            unit = es_inputs[index].unit

                    # Generate entry item.
                    es_entry = self.__generate_entry(unit, id, name, value)

                    # Add entry item to entries.
                    self.__entries.append(es_entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates and sort.
                indexes_split = sorted(list(set(indexes_split)))

                # If the length is grater then one.
                for index in range(len(indexes_split)):
                    if indexes_split[index] in self.__ES["id"]:

                        # Get ID of the entry item.
                        id = self.__ES["id"][indexes_split[index]]

                        # Create nama of the entry item.
                        name = self.__ES["name"] + indexes_split[index]

                        # Temporal fields.
                        value = ""
                        unit = ""

                        # Get value of the entry item.
                        if es_inputs[index] != None and es_inputs[index].isValid():
                            value = es_inputs[index].getValue()
                            unit = es_inputs[index].getUnit()

                        # Generate entry item.
                        es_entry = self.__generate_entry(unit, id, name, value)

                        # Add entry item to entries.
                        self.__entries.append(es_entry)

#endregion
