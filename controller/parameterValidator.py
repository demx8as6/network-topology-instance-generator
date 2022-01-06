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
import json
import jsonschema
import os
import os.path

class ParameterValidator:

  configFile = "config.json"
  config = {}
  configSchemaFile = os.path.dirname(os.path.realpath(__file__)) + "/../model/jsonSchema/configuration.schema.json"
  configSchema = {}
  error = ""
  valid = False

  # constructor 
  def __init__(self,args):
    self.args=args

    if len(self.args) > 1:
      self.configFile = args[1]

    if os.path.isfile(self.configFile) is False: 
      print("File", self.configFile, "does not exist.")
    else:
      with open(self.configFile) as configFileContent:
        self.config = json.load(configFileContent)

    if os.path.isfile(self.configSchemaFile) is False:
      print("File", self.configSchemaFile, "does not exist.")
    else:
      with open(self.configSchemaFile) as configSchemaFileContent:
        self.configSchema = json.load(configSchemaFileContent)

    # print(self.configSchema)
    # print(self.config)
    # jsonschema.validate(instance=self.config, schema=self.configSchema)
    self.valid = self.__isJsonValid(self.config, self.configSchema)

  def getConfigFile(self):
    return self.configFile

  def getConfiguration(self):
    return self.config
  
  def isValid(self):
    return self.valid

  def getError(self):
    return self.error

  # private

  def __isJsonValid(self, jsonData, jsonSchema):
    try:
        jsonschema.validate(instance=jsonData, schema=jsonSchema)
        self.error = "";
    except jsonschema.exceptions.ValidationError as err:
        self.error = err
        return False
    return True

