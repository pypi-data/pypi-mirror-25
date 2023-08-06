## Modbus Server and Client programs using Python-3
* server.py
* client.py

### Installation:
* sudo pip3 install modbus

### Usage Examples:
* sudo python3 -m modbus.server ...to run server
* python3 -m modbus.client ...to run client in commandline

### To run within another program or interpreter.
* from modbus import client
* c = client(host='localhost')
* r = c.read(FC=3, ADD=0, LEN=8)
* print("Received Data =", r)  
* c.write(FC=16, ADD=0, DAT=[11,22,333,4444]) ...DAT should be a list of values

