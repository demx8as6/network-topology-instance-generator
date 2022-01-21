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
Module containing a class for parameter validation
"""
import os
import os.path
import json
from typing import Dict
from xml.dom.minicompat import StringTypes
from xmlrpc.client import Boolean
import jsonschema


class ParameterValidator:
    """
    Class validating the configuration as input for the generator.
    """

    __config_file = "config.json"
    __configuration = {}
    __configuration_schema_file = os.path.dirname(os.path.realpath(
        __file__)) + "/../model/jsonSchema/configuration.schema.json"
    __config_schema = {}
    __error_messsage = ""
    __is_valid = False

    # constructor
    def __init__(self, args):
        self.args = args

        if len(self.args) > 1:
            self.__config_file = args[1]

        if os.path.isfile(self.__config_file) is False:
            print("File", self.__config_file, "does not exist.")
        else:
            with open(self.__config_file) as content:
                self.__configuration = json.load(content)

        if os.path.isfile(self.__configuration_schema_file) is False:
            print("File", self.__configuration_schema_file, "does not exist.")
        else:
            with open(self.__configuration_schema_file) as content:
                self.__config_schema = json.load(content)
        self.__is_valid = self.__is_json_valid(
            self.__configuration, self.__config_schema)

    def configuration_file(self) -> StringTypes:
        """
        Getter for the configuration filename.
        :return Filename (path) for the init configuration.
        """
        return self.__config_file

    def configuration(self) -> Dict:
        """
        Getter for the configuration as input parameter.
        :return Init configuration as Dict.
        """
        return self.__configuration

    def is_valid(self) -> Boolean:
        """
        Getter for the validation result.
        :return Init configuration as Dict.
        """
        return self.__is_valid

    def error_message(self) -> StringTypes:
        """
        Getter for the error message after validation process or an empty sting,
        when configuration is valid.
        :return Errormessage as string.
        """
        return self.__error_messsage

    # private

    def __is_json_valid(self, json_data, json_schema):
        """
        Method validating json against a schema
        """
        try:
            jsonschema.validate(instance=json_data, schema=json_schema)
            self.__error_messsage = ""
        except jsonschema.exceptions.ValidationError as err:
            self.__error_messsage = err
            return False
        return True
