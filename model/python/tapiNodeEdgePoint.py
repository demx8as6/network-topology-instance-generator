# Copyright 2021 highstreet technologies GmbH
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

class TapiNodeEdgePoint:

    nodeEdgePoint = {}
    config = {}

    # constructor
    def __init__(self, config):
        self.config = config
        self.nodeEdgePoint = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "interface-name",
                "value": config['nodeEdgePoint']['interface']
            }],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "link-port-role": "SYMMETRIC",
            "layer-protocol-name": "ETH",
            "supported-cep-layer-protocol-qualifier": [
                "tapi-dsr:DIGITAL_SIGNAL_TYPE_GigE"
            ],
            "link-port-direction": "BIDIRECTIONAL"
        }

    # getter

    def get(self):
        return self.nodeEdgePoint

    # methods
    def add(self, config):
        return self
