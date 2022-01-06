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
import uuid
from model.python.tapiTopologyContext import TapiTopologyContext

class TapiCommonContext:

  context = {}

  # constructor
  def __init__(self):
    self.context = {
      "tapi-common:context": {
          "uuid": str(uuid.uuid4()),
          "name": [{"value-name": "context-name",
                    "value": "Generated Topology"}]}}

  # getter
  def get(self):
      return self.context

  # methods
  def add(self,config):
    self.context["tapi-common:context"].update( TapiTopologyContext().add(config).get())
    return self