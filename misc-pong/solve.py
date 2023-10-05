import icmplib
from time import sleep
import sys

# TO RUN:
# `pip3 install -e icmplib` 


host = "18.191.205.48"
#host = "127.0.0.1"
file = "out.png"

sock = icmplib.ICMPv4Socket(privileged=False)
num = 0
c = "wb"
if len(sys.argv) == 2:
    num = int(sys.argv[1])
    c = "ab"

with open(file, c) as f:
    for seq in range(100000):
        num = num + 1
        req = icmplib.ICMPRequest(host, 0x1337, seq, payload_size=0)
        sock.send(req)
        reply = sock.receive(req, timeout=5)
        print(num)
        data_loc = 0x1C # offset into payload
        if len(reply._packet) <= data_loc:
            break
        data = reply._packet[data_loc:]
        f.write(data)

print(f"Took {num} pings")
print(f"Output flag data written to {file}")
