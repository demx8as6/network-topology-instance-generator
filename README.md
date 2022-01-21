# Network Topology Instance Generator 

This python project generates a network topology according 
[TAPI-Topology yang - v2.3.1](https://github.com/OpenNetworkingFoundation/TAPI/blob/v2.3.1/YANG/tapi-topology.yang).

Please note: The generator does not need to implement streaming or notification 
functions. The dependencies to tapi-notification and tapi-streaming were 
removed. 

Each network-function is represented as TAPI-Node which exposes interfaces to 
other network-functions or to management systems.

Therefore the Network Topology can cover 

 * Data Plane (also called User Plane), 
 * Synchronization Plane, 
 * Control Plane and
 * Management Plane.

Interface end-points of network-functions are represented as 
TAPI-Owned-Node-Edge-Points. TAPI-Links create a logical connection between 
TAPI-Owned-Node-Edge-Points of the same layer (or even more strict of the same 
layer-protocol-name).

## Prerequisites

```
sudo pip install jsonschema
```

## Generation Input

The generator consumes a json as input. The json defines the hierarchy of 
network-function types and its number of elements per parent.

Example:

``` json
{
  "network": {
    "name": "Test network",
    "pattern": {
      "o-du":2,
      "o-ru":3
    }
  }
}
```

The resulting network will include 2 network-functions of type "o-du". 
Each "o-du" is connected to 3 network-function instances of type "o-ru".

```
network
 +-- o-du-1
 |   +-- o-ru-11
 |   +-- o-ru-12
 |   +-- o-ru-13
 +-- o-du-2
     +-- o-ru-21
     +-- o-ru-22
     +-- o-ru-23
```
## Usage

```
python tapi_topology_generator.py config.json
```