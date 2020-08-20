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
from xml.dom.minidom import parseString

import dicttoxml

from services.http.request_handler import RequestHandler

from devices.pt.picons.io_board import IOBoard
from devices.vedicom.vdi3060.vdi3060 import VDI3060

from data.measurement import Measurement

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

    __TOGGLE_RELAY_1 = "ToggleRelay1"
    """Toggle relay 1 command key. Value: 1"""

    __TOGGLE_RELAY_2 = "ToggleRelay2"
    """Toggle relay 2 command key. Value: 1"""

    __TOGGLE_RELAY_3 = "ToggleRelay3"
    """Toggle relay 3 command key. Value: 1"""

    __TOGGLE_RELAY_4 = "ToggleRelay4"
    """Toggle relay 4 command key. Value: 1"""

    __PULSE_RELAY_1 = "PulseRelay1"
    """Pulse relay 1 command key. Value: 1 to 60[s]"""

    __PULSE_RELAY_2 = "PulseRelay2"
    """Pulse relay 2 command key. Value: 1 to 60[s]"""

    __PULSE_RELAY_3 = "PulseRelay3"
    """Pulse relay 3 command key. Value: 1 to 60[s]"""

    __PULSE_RELAY_4 = "PulseRelay4"
    """Pulse relay 4 command key. Value: 1 to 60[s]"""

    __RO = {"key":"RelayOutputs", "unit":"LogicLevel", "identifier":{"1": "0", "2": "1", "3": "2", "4": "3"}}
    """Relay outputs descriptor."""

    __DI = {"key":"DigitalInputs", "unit":"LogicLevel", "identifier":{"1": "4", "2": "5", "3": "6", "4": "7", "5": "8", "6": "9"}}
    """Digital inputs descriptor."""

    __CI = {"key":"CounterInputs", "unit":"Count", "identifier":{"1":"10", "2":"11"}}
    """Counters inputs descriptor."""

    __AI = {"key":"AnalogInputs", "unit":"V", "identifier":{"1": "12", "2":"13", "3":"14", "4":"15", "5":"16", "6":"17", "7":"18", "8":"19"}}
    """Analog inputs descriptor."""

    __ES = {"key":"ElectronicScales", "name":"ElectronicScale", "identifier":{"1": "20"}}
    """Electronic scales descriptor."""

    __PROTOCOL_VERSION = "16.11.0.1"
    """Protocol version."""

    __STATE_LOW = "0"
    """Text representation of logic level 0."""

    __STATE_HIGH = "1"
    """Text representation of logic level 1."""

    __io_board = IOBoard()
    """IO board."""

    __entries = []
    """Entries"""

#endregion

#region Protected Methods

    def _do_page(self):

        # Container.
        container = dict()

        # Clear the entries.
        self.__entries.clear()

        # Clear the body.
        page_body = ""

        # Parse the URL path.
        parsed_url = parse.urlparse(self.path)

        # Check is there arguments.
        if parsed_url.query is not None and parsed_url.query != "":

            ucq_dict = parse.parse_qs(parsed_url.query)
            query_dict = dict([(str(key), str(value[0])) for key, value in ucq_dict.items()])

            self.__do_ro(query_dict)
            self.__do_di(query_dict)
            self.__do_ci(query_dict)
            self.__do_ai(query_dict)
            self.__do_es(query_dict)


        # Create XML structure.
        container["ProtocolVersion"] = self._PROTOCOL_VERSION
        container["Device"] = self._settings.device_name
        container["Entries"] = self.__entries

        page_body = dicttoxml.dicttoxml(container, custom_root="Monitor", attr_type=False)

        dom = parseString(page_body)
        page_body_bu = dom.toprettyxml()

        return page_body_bu.encode("utf-8")

#endregion

#region Private Methods

    def __generate_entry(self, units, identifier, name, value):
        """Generate entry.

        Parameters
        ----------
        units : str
            Units of the measurement in the entry.
        identifier : int
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
        entry["ID"] = identifier
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

                for key, value in enumerate(self.__RO["identifier"]):

                    # Get ID of the entry item.
                    identifier = self.__RO["identifier"][str(key + 1)]

                    # Get value of the entry item.
                    value = self.__STATE_HIGH if relay_outputs[key] else self.__STATE_LOW

                    # Create name of the entry item.
                    name = self._settings.ro_name(key + 1)

                    # Generate entry item.
                    entry = self.__generate_entry(self.__RO["unit"], identifier, name, value)

                    # Add entry item to entries.
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_spited = indexes.split(",")

                # Remove duplicates and sort.
                indexes_spited = sorted(list(set(indexes_spited)))

                # If the length is grater then one.
                for key, value in enumerate(indexes_spited):

                    if indexes_spited[key] in self.__RO["identifier"]:

                        # Get ID of the entry item.
                        identifier = self.__RO["identifier"][indexes_spited[key]]

                        # Get value of the entry item.
                        value = self.__STATE_HIGH if relay_outputs[key] else self.__STATE_LOW

                        # Create name of the entry item.
                        name = self._settings.ro_name(key + 1)

                        # Generate entry item.
                        entry = self.__generate_entry(self.__RO["unit"], identifier, name, value)

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

                for key, value in enumerate(self.__DI["identifier"]):

                    # Get ID of the entry item.
                    identifier = self.__DI["identifier"][str(key + 1)]

                    # Get value of the entry item.
                    value = self.__STATE_HIGH if digital_inputs[key] else self.__STATE_LOW

                    # Create name of the entry item.
                    name = self._settings.di_name(key + 1)

                    # Generate entry item.
                    entry = self.__generate_entry(self.__DI["unit"], identifier, name, value)

                    # Add entry item to entries.
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove dublicates and sort.
                indexes_split = sorted(list(set(indexes_split)))

                # If the length is grater then one.
                for key, value in enumerate(indexes_split):

                    if indexes_split[key] in self.__DI["identifier"]:

                        # Get ID of the entry item.
                        identifier = self.__DI["identifier"][indexes_split[key]]

                        # Get value of the entry item.
                        value = self.__STATE_HIGH if digital_inputs[key] else self.__STATE_LOW

                        # Create name of the entry item.
                        name = self._settings.di_name(key + 1)

                        # Generate entry item.
                        entry = self.__generate_entry(self.__DI["unit"], identifier, name, value)

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

                for key, value in enumerate(self.__CI["identifier"]):

                    # Get ID of the entry item.
                    identifier = self.__CI["identifier"][str(key + 1)]

                    # Get value of the entry item.
                    value = counters_inputs[key]

                    # Create name of the entry item.
                    name = self._settings.ci_name(key + 1)

                    # Generate entry item.
                    entry = self.__generate_entry(self.__CI["unit"], identifier, name, value)

                    # Add entry item to entries.
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates and sort.
                indexes_split = sorted(list(set(indexes_split)))

                # If the length is grater then one.
                for key, value in enumerate(indexes_split):

                    if indexes_split[key] in self.__CI["identifier"]:

                        # Get ID of the entry item.
                        identifier = self.__CI["identifier"][indexes_split[key]]

                        # Get value of the entry item.
                        value = counters_inputs[key]

                        # Create name of the entry item.
                        name = self._settings.ci_name(key + 1)

                        # Generate entry item.
                        entry = self.__generate_entry(self.__CI["unit"], identifier, name, value)

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
                for key, value in enumerate(self.__AI["identifier"]):

                    # Get ID of the entry item.
                    identifier = self.__AI["identifier"][str(key + 1)]

                    # Get value of the entry item.
                    value = analog_inputs[key]

                    # Create name of the entry item.
                    name = self._settings.ai_name(key + 1)

                    # Generate entry item.
                    entry = self.__generate_entry(self.__AI["unit"], identifier, name, value)

                    # Add entry item to entries.
                    self.__entries.append(entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates.
                indexes_split = list(set(indexes_split))

                # If the length is grater then one.
                for key, value in enumerate(indexes_split):

                    if indexes_split[key] in self.__AI["identifier"]:

                        # Get ID of the entry item.
                        identifier = self.__AI["identifier"][indexes_split[key]]

                        # Get value of the entry item.
                        value = analog_inputs[key]

                        # Create name of the entry item.
                        name = self._settings.ai_name(key + 1)

                        # Generate entry item.
                        entry = self.__generate_entry(self.__AI["unit"], identifier, name, value)

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

            # Data container.
            es_inputs = []
            es_inputs.append(measurement)

            # If the key is all then get all electronic scales.
            if indexes == "all":
                for index in range(len(self.__ES["identifier"])):

                    # Get ID of the entry item.
                    identifier = self.__ES["identifier"][str(index + 1)]

                    # Create name of the entry item.
                    name = self.__ES["name"] + str(index + 1)

                    # Temporal fields.
                    value = ""
                    unit = ""

                    # Get value of the entry item.
                    if es_inputs[index] is not None:
                        if es_inputs[index].is_valid:
                            value = es_inputs[index].value
                            unit = es_inputs[index].unit

                    # Generate entry item.
                    es_entry = self.__generate_entry(unit, identifier, name, value)

                    # Add entry item to entries.
                    self.__entries.append(es_entry)

            # If the key is array.
            elif indexes != "":

                # Split by coma.
                indexes_split = indexes.split(",")

                # Remove duplicates and sort.
                indexes_split = sorted(list(set(indexes_split)))

                # If the length is grater then one.
                for key, value in enumerate(indexes_split):
                    if indexes_split[key] in self.__ES["identifier"]:

                        # Get ID of the entry item.
                        identifier = self.__ES["identifier"][indexes_split[key]]

                        # Create name of the entry item.
                        name = self.__ES["name"] + indexes_split[key]

                        # Temporal fields.
                        value = ""
                        unit = ""

                        # Get value of the entry item.
                        if es_inputs[key] is not None and es_inputs[key].is_valid:
                            value = es_inputs[key].value
                            unit = es_inputs[key].unit

                        # Generate entry item.
                        es_entry = self.__generate_entry(unit, identifier, name, value)

                        # Add entry item to entries.
                        self.__entries.append(es_entry)

#endregion
