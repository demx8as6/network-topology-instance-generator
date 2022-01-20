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
import uuid
from model.python.tapiNode import TapiNode
from model.python.tapiNodeEdgePoint import TapiNodeEdgePoint


class TapiNodeORu(TapiNode):

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)

        # add OFHM/OAM NetConf Provider interface
        o1NcProviderConfig = {"nodeEdgePoint": {
            "interface": "open-fronthaul-m-plane", "protocol": "NETCONF", "role": "provider"}}
        o1NcProvider = TapiNodeEdgePoint(o1NcProviderConfig)
        self.add(o1NcProvider)

        # add air provider interface
        airProviderConfig = {"nodeEdgePoint": {
            "interface": "air", "protocol": "unknown", "role": "provider"}}
        airProvider = TapiNodeEdgePoint(airProviderConfig)
        self.add(airProvider)
