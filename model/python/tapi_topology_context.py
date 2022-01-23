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
Module for the TAPI Topology Context
"""
from typing import Dict, List
from model.python.tapi_topology import TapiTopology
from model.python.top import Top


class TapiTopologyContext(Top):
    """
    Class providing a TAPI Topology Context object
    """

    __data: dict = {
        "tapi-topology:topology-context": {
            "topology": []}}
    __tapi_topology = []

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context initail
        configuration.
        :return TAPI Topology Context configuration as json object.
        """
        return self.__configuration

    def cytoscape(self) -> Dict[str, List]:
        """
        Getter returning the object for topology visualization.
        :return Link configuration.
        """
        result = {"elements": []}
        for instance in self.__tapi_topology:
            # well, results in a singel topology only
            result.update(instance.cytoscape())
        return result

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Topology Context as json object.
        """
        return self.__data

    def name(self) -> str:
        """
        Getter returning the container name.
        :return Static string
        """
        return "tapi-topology:topology-context"

    def identifier(self) -> str:
        """
        Getter returning the container name which acts as identifier
        :return Static string
        """
        return self.name()

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Topology Context as json object.
        """
        return self.data()

    # methods
    def add(self, configuration) -> 'TapiTopologyContext':
        """
        Adds a TAPI Topology to the TAPI Topology Context
        :param configuration: An input parameter as json object.
        :return This object.
        """
        topology = TapiTopology(configuration)
        self.__tapi_topology.append(topology)
        self.__data["tapi-topology:topology-context"]["topology"].append(
            topology.json())
        return self
