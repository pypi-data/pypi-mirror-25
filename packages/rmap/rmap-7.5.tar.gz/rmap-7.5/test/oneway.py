# create JSON-RPC client
import rmap.jsonrpc as jsonrpc
import time

server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(radio=False,notification=False), jsonrpc.TransportSERIAL(port="/dev/ttyUSB0",baudrate=115200, logfunc=jsonrpc.log_file("myrpc.log")))

while True:
    # call a remote-procedure (with positional parameters)
    result = server.single(did=10,dstunit=0,onoff=True)
    print result
    #time.sleep(2)
    result = server.single(did=10,dstunit=0,onoff=False)
    #time.sleep(2)
