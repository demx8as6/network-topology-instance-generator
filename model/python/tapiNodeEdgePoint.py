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
from model.python.top import Top


class TapiNodeEdgePoint(Top):

    data = {}
    config = {"nodeEdgePoint": {"interface": "unknown-interface",
                                "protocol": "unknown-protocol",
                                "role": "consumer"}}

    # constructor
    def __init__(self, config):
        self.config = config
        self.data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "interface-name",
                "value": self.getName()
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
            "termination-state": self.getTerminationState(),
            "termination-direction": self.getTerminationDirection()
        }

    # getter

    def getData(self):
        return self.data

    def getConfiguration(self):
        return self.config

    def getName(self):
        items = (self.config['nodeEdgePoint']['interface'],
                 self.config['nodeEdgePoint']['protocol'],
                 self.config['nodeEdgePoint']['role'])
        return "-".join(items).lower()

    def getTerminationDirection(self):
        value = "BIDIRECTIONAL"
        map = {
            "consumer": "SINK",
            "provider": "SOURCE"
        }
        if self.config['nodeEdgePoint']['role'].lower() in map:
            return map[self.config['nodeEdgePoint']['role'].lower()]        
        return value

    def getTerminationState(self):
        return "PERMANENTLY_TERMINATED"

    def toJson(self):
        return self.getData()
