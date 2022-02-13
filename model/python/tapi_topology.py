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
Module containing the main class for this project for a TAPI Topology.
"""
import uuid
from typing import Dict, List, Union
from lxml import etree

from model.python.top import Top
from model.python.tapi_node import TapiNode
from model.python.tapi_node_smo import TapiNodeSmo
from model.python.tapi_node_o_cloud import TapiNodeOCloud
from model.python.tapi_node_near_rt_ric import TapiNodeNearRtRic
from model.python.tapi_node_o_cu_cp import TapiNodeOCuCp
from model.python.tapi_node_o_cu_up import TapiNodeOCuUp
from model.python.tapi_node_o_du import TapiNodeODu
from model.python.tapi_node_fronthaul_gateway import TapiNodeFronthaulGateway
from model.python.tapi_node_o_ru import TapiNodeORu
from model.python.tapi_node_user_equipment import TapiNodeUserEquipment
from model.python.tapi_link import TapiLink


class TapiTopology(Top):
    """
    Class representing a TAPI Topology
    """

    __data: Dict[str, Union[str, List[Union[Dict, TapiNode, TapiLink]]]] = None
    __configuration: dict = None

    # constructor
    def __init__(self, configuration: dict):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "network-name",
                "value": configuration['network']['name']}],
            "layer-protocol-name": ["ETH"],
            "node": [],
            "link": []}

        topology_structure: dict = configuration['network']['pattern']
        network_function_type: str = next(iter(topology_structure))
        count: int = configuration['network']['pattern'][network_function_type]

        if network_function_type == "smo":
            self.__create_smos(None, topology_structure, count)
        elif network_function_type == "near-rt-ric":
            self.__create_near_rt_rics(None, topology_structure, count)
        elif network_function_type == "o-cu":
            self.__create_o_cus(None, topology_structure, count)
        elif network_function_type == "o-du":
            self.__create_o_dus(None, topology_structure, count)
        elif network_function_type == "o-ru":
            self.__create_o_rus(None, topology_structure, count)
        elif network_function_type == "ue":
            self.__create_ues(None, topology_structure, count)
        else:
            print("Unknown network function type", network_function_type)

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology configuration.
        :return TAPI Topology configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology.
        :return TAPI Topology as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Topology identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def name(self) -> str:
        """
        Getter for TAPI Topology name. The TAPI topology is a representation of
        the network. Therefore, the TAPI Topology name has the same value as the
        Network name.
        :return TAPI Topology name as string.
        """
        return self.__configuration['network']['name']

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology.
        :return TAPI Topology Context as json object.
        """
        result = self.data().copy()

        # nodes handling
        result["node"] = []
        for node in self.__data["node"]:
            result["node"].append(node.json())

        # link handling
        result["link"] = []
        for link in self.__data["link"]:
            result["link"].append(link.json())

        return result

    def svg(self, svg_x: int, svg_y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Topology Context.
        :return TAPI Topology Context as svg object.
        """
        group = etree.Element("g")
        desc = etree.Element("desc")
        desc.text = "\n TAPI Topology \n id: " + \
            self.identifier()  # + "\n name: " + self.name()
        group.append(desc)

        # nodes handling
        index_per_type: Dict = {}
        svg_nodes = []
        for node in self.__data["node"]:
            if type(node) in index_per_type:
                index_per_type[type(node)] = index_per_type[type(node)] + 1
            else:
                index_per_type[type(node)] = 0
            index = index_per_type[type(node)]
            node_x = svg_x + \
                index*self.__svg_dynamic_x_offset_by_node_type(type(node)) + \
                self.__svg_static_x_offset_by_node_type(type(node))
            node_y = svg_y + self.__svg_y_offset_by_node_type(type(node))
            svg_nodes.append(node.svg(node_x, node_y))
            # group.append(node.svg(node_x, node_y))

        # handling and drawing links
        for link in self.__data["link"]:
            group.append(link.svg(0, 0))

        # drawing nodes
        for svg_node in svg_nodes:
            group.append(svg_node)

        return group

    def __svg_static_x_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        pattern = self.configuration()['network']['pattern']
        x_mapping: Dict[type, int] = {
            TapiNodeSmo: 3 * self.FONTSIZE,
            TapiNodeOCloud: 3 * self.FONTSIZE,
            TapiNodeNearRtRic: 3 * self.FONTSIZE,
            TapiNodeOCuCp: 3 * self.FONTSIZE,
            TapiNodeOCuUp: 3 * self.FONTSIZE,
            TapiNodeODu: 2 * self.FONTSIZE,
            TapiNodeFronthaulGateway: 2 * self.FONTSIZE,
            TapiNodeORu: 2 * self.FONTSIZE,
            TapiNodeUserEquipment: 0
        }
        if "near-rt-ric" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['near-rt-ric']
        if "o-cu" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-cu']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-cu']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-cu']
        if "o-du" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-du']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-du']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-du']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['o-du']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['o-du']
        if "fronthaul-gateway" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['fronthaul-gateway']
        if "o-ru" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-ru']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['o-ru']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['o-ru']
            x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] * \
                pattern['o-ru']
        if "user-equipment" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['user-equipment']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['user-equipment']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['user-equipment']
            x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] * \
                pattern['user-equipment']
            x_mapping[TapiNodeORu] = x_mapping[TapiNodeORu] * \
                pattern['user-equipment']

        x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] - 1.5 * 2*self.FONTSIZE
        x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] - \
            1 * 2*self.FONTSIZE
        x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] - \
            1 * 2*self.FONTSIZE
        x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] - \
            6 * 2 * self.FONTSIZE
        x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] + \
            2 * 2 * self.FONTSIZE
        x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] + \
            1.5 * 2*self.FONTSIZE
        x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] + 1.5 * 2*self.FONTSIZE

        if node_type in x_mapping:
            return x_mapping[node_type]
        return 0

    def __svg_dynamic_x_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        pattern = self.configuration()['network']['pattern']
        x_mapping: Dict[type, int] = {
            TapiNodeSmo: 3 * self.FONTSIZE,
            TapiNodeOCloud: 3 * self.FONTSIZE,
            TapiNodeNearRtRic: 3 * self.FONTSIZE,
            TapiNodeOCuCp: 3 * self.FONTSIZE,
            TapiNodeOCuUp: 3 * self.FONTSIZE,
            TapiNodeODu: 3 * self.FONTSIZE,
            TapiNodeFronthaulGateway: 6 * self.FONTSIZE,
            TapiNodeORu: 3 * self.FONTSIZE,
            TapiNodeUserEquipment: 2 * self.FONTSIZE
        }
        if "smo" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * pattern['smo']
        if "o-cloud" in pattern:
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-cloud']
        if "near-rt-ric" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['near-rt-ric']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['near-rt-ric']
        if "o-cu" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-cu']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-cu']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-cu']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['o-cu']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['o-cu']
        if "o-du" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-du']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-du']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-du']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['o-du']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['o-du']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['o-du']
        if "fronthaul-gateway" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['fronthaul-gateway']
            x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] * \
                pattern['fronthaul-gateway']
        if "o-ru" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['o-ru']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['o-ru']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['o-ru']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['o-ru']
            x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] * \
                pattern['o-ru']
            x_mapping[TapiNodeORu] = x_mapping[TapiNodeORu] * \
                pattern['o-ru']
        if "user-equipment" in pattern:
            x_mapping[TapiNodeSmo] = x_mapping[TapiNodeSmo] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCloud] = x_mapping[TapiNodeOCloud] * \
                pattern['user-equipment']
            x_mapping[TapiNodeNearRtRic] = x_mapping[TapiNodeNearRtRic] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCuCp] = x_mapping[TapiNodeOCuCp] * \
                pattern['user-equipment']
            x_mapping[TapiNodeOCuUp] = x_mapping[TapiNodeOCuUp] * \
                pattern['user-equipment']
            x_mapping[TapiNodeODu] = x_mapping[TapiNodeODu] * \
                pattern['user-equipment']
            x_mapping[TapiNodeFronthaulGateway] = x_mapping[TapiNodeFronthaulGateway] * \
                pattern['user-equipment']
            x_mapping[TapiNodeORu] = x_mapping[TapiNodeORu] * \
                pattern['user-equipment']
            x_mapping[TapiNodeUserEquipment] = x_mapping[TapiNodeUserEquipment] * \
                pattern['user-equipment']

        if node_type in x_mapping:
            return x_mapping[node_type]
        return 0

    def __svg_y_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        offset = 11*self.FONTSIZE
        y_mapping: Dict[type, int] = {
            TapiNodeSmo: 0 * offset,
            TapiNodeOCloud: 1 * offset,
            TapiNodeNearRtRic: 2 * offset,
            TapiNodeOCuCp: 3 * offset - 20,
            TapiNodeOCuUp: 3 * offset + 20,
            TapiNodeODu: 4 * offset,
            TapiNodeFronthaulGateway: 5 * offset,
            TapiNodeORu: 6 * offset,
            TapiNodeUserEquipment: 7 * offset
        }
        if node_type in y_mapping:
            return y_mapping[node_type]
        return 0

    # methods
    def add_node(self, node: TapiNode):
        """
        Method adding a TAPI node to TAPI Topology.
        :return TAPI Topology object.
        """
        self.__data["node"].append(node)
        return self

    def add_link(self, link: TapiLink):
        """
        Method adding a TAPI node to TAPI Topology.
        :return TAPI Topology object.
        """
        self.__data["link"].append(link)
        return self

    def __create_smos(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "smo"
        next_type = "near-rt-ric"
        for local_id in range(count):
            prefix = ""

            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-sc-topology-common:"+current_type}}
            node = TapiNodeSmo(parent, config)
            self.add_node(node)

            # add O-Clouds
            if "o-cloud" in topology_structure:
                structure = topology_structure.copy()
                self.__create_o_clouds(
                    node, structure, structure["o-cloud"])

            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure["o-cloud"]
                if current_type in structure:
                    del structure[current_type]
                self.__create_near_rt_rics(
                    node, structure, structure[next_type])

        return self

    def __create_o_clouds(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-cloud"
        for local_id in range(count):
            # add node
            prefix = ""
            if parent is not None:
                prefix = parent.json()["name"][1]["value"]
            function = "o-ran-sc-topology-common:"+current_type
            node_configuration = {"node": {"localId": prefix + str(local_id),
                                           "type": current_type,
                                           "function": function}}
            node = TapiNodeOCloud(parent, node_configuration)
            self.add_node(node)

            # add links
            # O2
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o2-rest",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))
        return self

    def __create_near_rt_rics(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "near-rt-ric"
        next_type = "o-cu"
        for local_id in range(count):
            # add node
            prefix = ""
            if parent is not None:
                prefix = parent.json()["name"][1]["value"]
            function = "o-ran-sc-topology-common:"+current_type
            node_configuration = {"node": {"localId": prefix + str(local_id),
                                           "type": current_type,
                                           "function": function}}
            node = TapiNodeNearRtRic(parent, node_configuration)
            self.add_node(node)

            # add links
            # A1
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "a1-rest",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 NETCONF
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-netconf",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 FILE
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-file",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 VES
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-ves",
                "provider": parent,
                "consumer": node
            }
            self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_cus(node, structure, structure[next_type])

        return self

    def __function_identity(self, function_type: str, plane: str) -> str:
        """
        Method to calculate the Function IDENTITY
        """
        return "".join([
            "o-ran-sc-topology-common:",
            function_type,
            "-",
            plane
        ])

    def __create_o_cus(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-cu"
        next_type = "o-du"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]

            node: Dict[str, Union[TapiNodeOCuCp, TapiNodeOCuUp]] = {}
            for plane in ["cp", "up"]:
                config = {"node": {"localId": prefix + str(local_id),
                                   "type": "-".join([current_type, plane]),
                                   "function": self.__function_identity(current_type, plane)}}
                classes: Dict[str, Union[TapiNodeOCuCp, TapiNodeOCuUp]] = {
                    "cp": TapiNodeOCuCp,
                    "up": TapiNodeOCuUp}
                node[plane] = classes[plane](parent, config)
                self.add_node(node[plane])

                # add links
                # E2
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "e2-rest",
                    "provider": node[plane],
                    "consumer": parent
                }
                self.add_link(TapiLink(link_configuration))

                # O1 NETCONF
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-netconf",
                    "provider": node[plane],
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 FILE
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-file",
                    "provider": node[plane],
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 VES
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-ves",
                    "provider": parent.parent(),
                    "consumer": node[plane]
                }
                self.add_link(TapiLink(link_configuration))

            # continue
            # E1 Interface between O-CU-UP and O-CU-CP
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "e1-unknown",
                "provider": node["up"],
                "consumer": node["cp"]
            }
            self.add_link(TapiLink(link_configuration))

            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_dus(
                    node, structure, structure[next_type])
        return self

    def __create_o_dus(self, parents: Dict[str, TapiNode], topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-du"
        next_type = "fronthaul-gateway"
        for local_id in range(count):
            prefix = "000"
            if parents["cp"] is not None:
                prefix = parents["cp"].data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-sc-topology-common:"+current_type}}
            node = TapiNodeODu(parents["cp"], config)
            self.add_node(node)

            for plane, parent in parents.items():

                # add links
                # E2
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "e2-rest",
                    "provider": node,
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 NETCONF
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-netconf",
                    "provider": node,
                    "consumer": parent.parent().parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 FILE
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-file",
                    "provider": node,
                    "consumer": parent.parent().parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 VES
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-ves",
                    "provider": parent.parent().parent(),
                    "consumer": node
                }
                self.add_link(TapiLink(link_configuration))

                # F1 User Plane or Control Plane
                interfaces: Dict[str, str] = {"cp": "f1-c", "up": "f1-u"}
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": interfaces[plane]+"-unknown",
                    "provider": node,
                    "consumer": parent
                }
                self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_fronthaul_gateways(
                    node, structure, structure[next_type])
        return self

    def __create_fronthaul_gateways(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "fronthaul-gateway"
        next_type = "o-ru"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-sc-topology-common:"+current_type}}
            node = TapiNodeFronthaulGateway(parent, config)
            self.add_node(node)

            # add links

            # Eth NBI
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "oam-netconf",
                "provider": node,
                "consumer": parent.parent().parent().parent()
            }
            self.add_link(TapiLink(link_configuration))

            # Eth SBI
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "eth-ofh",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_rus(node, structure, structure[next_type])
        return self

    def __create_o_rus(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-ru"
        next_type = "user-equipment"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-sc-topology-common:"+current_type}}
            node = TapiNodeORu(parent, config)
            self.add_node(node)

            # add links

            # O1 NETCONF
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "ofh-netconf",
                "provider": node,
                "consumer": parent.parent().parent().parent().parent()
            }
            self.add_link(TapiLink(link_configuration))

            # OFH M-Plane to O-DU via fronthaul-gateway
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "ofh-netconf",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_ues(node, structure, structure[next_type])
        return self

    def __create_ues(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "user-equipment"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-sc-topology-common:"+current_type}}
            node = TapiNodeUserEquipment(parent, config)
            self.add_node(node)

            # add links
            # Uu unknown
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "uu-unknown",
                "provider": parent,
                "consumer": node
            }
            self.add_link(TapiLink(link_configuration))

            if "key" in topology_structure:
                print("Implement missing topology level.")

        return self
