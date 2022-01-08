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

class TapiNode:

    node = {}
    config = {}

    # constructor
    def __init__(self, config):
        self.config = config
        self.node = {
            "uuid": str(uuid.uuid4()),
            "name": [
                {
                    "value-name": "topology-node-name",
                    "value": config['node']['type'] + "-" + str(config['node']['localId'])
                },
                {
                    "value-name": "topology-node-local-id",
                    "value": config['node']['localId']
                }
            ],
            "owned-node-edge-point": [],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "layer-protocol-name": ["ETH"],
            "cost-characteristic": [
                {
                    "cost-name": "cost",
                    "cost-algorithm": "alg1",
                    "cost-value": "value-1"
                }
            ],
            "latency-characteristic": [{
                "traffic-property-name": "property-1",
                "queing-latency-characteristic": "queue-1",
                "fixed-latency-characteristic": "latency-1",
                "jitter-characteristic": "jitter-1",
                "wander-characteristic": "wander-1"
            }],
            "o-ran-topology:function": config['node']['function'],
            "o-ran-topology:geolocation": {
                "longitude": "0",
                "latitude": "0",
                "altitude": "20000"
            }
        }

    # getter
    def get(self):
        return self.node

    def getFunction(self):
        return self.config['node']['function']

    def getFunctionLabel(self):
        map = {
            "o-ran-common-identity-refs:smo-function": "SMO",
            "o-ran-common-identity-refs:near-rt-ric-function": "Near-RT-RIC",
            "o-ran-common-identity-refs:o-cu-function": "O-CU",
            "o-ran-common-identity-refs:o-cu-cp-function": "O-CU-CP",
            "o-ran-common-identity-refs:o-cu-up-function": "O-CU-UP",
            "o-ran-common-identity-refs:o-du-function": "O-DU",
            "o-ran-common-identity-refs:o-ru-function": "O-RU",
            "o-ran-common-identity-refs:user-equipment-function": "UE"
        }
        if map[self.getFunction()]:
            return map[self.getFunction()]
        else:
            return self.getFunction()

    # methods
    def add(self, nep):
        self.node['owned-node-edge-point'].append(nep)
        return self
