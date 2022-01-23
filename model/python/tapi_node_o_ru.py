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
Module containing a class representing an O-RAN Radio Unit as TAPI Node.
"""
from model.python.tapi_node import TapiNode
from model.python.tapi_node_edge_point import TapiNodeEdgePoint


class TapiNodeORu(TapiNode):
    """
    Class representing a O-RAN Radio Unit as TAPI Node.
    """

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)

        # add OpenFronthaul Management Plane/OAM NetConf Provider interface
        nep_configuration = {
            "parent": parent.identifier(),
            "nodeEdgePoint": {
                "interface": "open-fronthaul-m-plane", "protocol": "NETCONF", "role": "provider"
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

        # add air provider interface
        nep_configuration = {
            "parent": parent.identifier(),
            "nodeEdgePoint": {
                "interface": "uu", "protocol": "unknown", "role": "provider"
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))