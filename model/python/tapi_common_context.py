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
Module for a class representing a TAPI Common Context
"""
import uuid
from model.python.tapi_topology_context import TapiTopologyContext
from model.python.top import Top


class TapiCommonContext(Top):
    """
    Class representing a TAPI Common Context object.
    """

    __data: dict = {
        "tapi-common:context": {
            "uuid": str(uuid.uuid4()),
            "name": [{"value-name": "context-name",
                      "value": "Generated Topology"}]}}

    # getter
    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Common Context as json object.
        """
        return self.__data

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Common Context as json object.
        """
        return self.data()

    # methods
    def add(self, configuration: dict):
        """
        Adds a TAPI Topology Context to the TAPI Common Context
        :param configuration: An input parameter as json object.
        :return This object.
        """
        self.data()["tapi-common:context"].update(
            TapiTopologyContext().add(configuration).json())
        return self
