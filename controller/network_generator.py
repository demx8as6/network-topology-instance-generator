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
Module containing the Generator class.
"""
from model.python.tapi_common_context import TapiCommonContext

class TopologyGenerator:
    """
    Class containing all methods to generate a TAPI topology.
    The generation process is influenced by a configuration in json format.
    """

    __configuration: dict = {}
    __topology: dict = {}

    # constructor
    def __init__(self, configuration: dict):
        self.__configuration = configuration

    # getters
    def topology(self) -> TapiCommonContext:
        """
        Getter returning the topology
        :return A TapiCommonContext Object
        """
        return self.__topology

    # returns a JSON serializable object
    def generate(self) -> TapiCommonContext:
        """
        Method to start the generation process.
        :return The TapiCommonContext object.
        """
        self.__topology = TapiCommonContext().add(self.__configuration)
        return self.__topology
