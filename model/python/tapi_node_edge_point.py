# Copyright 2022 highstreet technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python
"""
Module containing a class representing a TAPI Node Edge Point
"""
from typing import Dict, Union
import uuid
from model.python.top import Top


class TapiNodeEdgePoint(Top):
    """
    Class representing a TAPI Node Edge Point object
    """

    __data: dict = {}
    __configuration: dict = {
        "parent": "unknown",
        "nodeEdgePoint": {
            "interface": "unknown-interface",
            "protocol": "unknown-protocol",
            "role": "consumer"
        }
    }

    # constructor
    def __init__(self, configuration: dict):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "interface-name",
                "value": self.name()
            }],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "link-port-role": "SYMMETRIC",
            "layer-protocol-name": "ETH",
            "supported-cep-layer-protocol-qualifier": [
                "tapi-dsr:DIGITAL_SIGNAL_TYPE_GigE"
            ],
            "link-port-direction": "BIDIRECTIONAL",
            "termination-state": self.termination_state(),
            "termination-direction": self.termination_direction()
        }

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point intiail
        configuration.
        :return TAPI Node Edge Point configuration as json object.
        """
        return self.__configuration

    def cytoscape(self) -> Dict[str, Union[str, Dict]]:
        """
        Getter returning the object for topology visualization.
        :return Cytoscape Element.
        """
        return {
            "group": "nodes",
            "data": {
                "id": self.identifier(),
                "parent": self.parent(),
                "name": self.name()
            }
        }

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node Edge Point identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.data()

    def name(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point.
        :return TAPI Node Edge Point name as String.
        """
        items = (self.__configuration['nodeEdgePoint']['interface'],
                 self.__configuration['nodeEdgePoint']['protocol'],
                 self.__configuration['nodeEdgePoint']['role'])
        return "-".join(items).lower()

    def parent(self) -> str:
        """
        Getter returning the identifier the the TAPI Node hosting the Node
        Edge Point.
        :return Identifier of the TAPI Node containing this NEP.
        """
        return self.__configuration["parent"]

    def termination_direction(self) -> str:
        """
        Getter returning the TAPI Node Edge Point direction.
        :return TAPI Node Edge Point direction as String.
        """
        value = "BIDIRECTIONAL"
        mapping = {
            "consumer": "SINK",
            "provider": "SOURCE"
        }
        if self.__configuration['nodeEdgePoint']['role'].lower() in mapping:
            return mapping[self.__configuration['nodeEdgePoint']['role'].lower()]
        return value

    def termination_state(self) -> str:
        """
        Getter returning the TAPI Node Edge Point state.
        :return TAPI Node Edge Point state as String.
        """
        return "PERMANENTLY_TERMINATED"
