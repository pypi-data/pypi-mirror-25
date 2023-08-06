## Modbus Server and Client programs using Python-3
* server.py
* client.py

### Usage Examples:
* Copy the 'modbus' directory to /usr/lib/python3/dist-packages/
* sudo python3 -m modbus.server -- to run server
* python3 -m modbus.client -- to run client in commandline

### To run within another program or interpreter.
* import modbus
* c = modbus.client('localhost')
* r = c.read(FC=3,ADD=0,LEN=8)
* print("Received Data =", r)  
* c.write(FC=16,ADD=0,DAT=[11,22,333,4444])

