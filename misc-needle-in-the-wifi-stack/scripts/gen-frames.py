#!/usr/bin/env python

from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, wrpcap, hexdump
import base64
import random
import sys

if len(sys.argv) < 4:
    print('needs args')
    exit(1)

IFILE = sys.argv[1]
FLAGFILE = sys.argv[2]
OFILE = sys.argv[3]

with open(IFILE, 'r') as inf:
    leetnames = inf.readlines()
with open(FLAGFILE, 'r') as flagf:
    flagname = flagf.readlines()[0]
leetnames.insert(63, flagname)

frames = []

for name in leetnames:
    b64name = base64.b64encode(bytes(name, 'ascii'))
    # https://www.4armed.com/blog/forging-wifi-beacon-frames-using-scapy/
    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2='22:22:22:22:22:22', addr3='33:33:33:33:33:33')
    beacon = Dot11Beacon(cap='ESS+privacy')
    essid = Dot11Elt(ID='SSID', info=b64name, len=len(b64name))

    rsn = Dot11Elt(ID='RSNinfo', info=(
        b'\x01\x00'              # RSN Version 1
        b'\x00\x0f\xac\x02'      # Group Cipher Suite : 00-0f-ac TKIP
        b'\x02\x00'              # 2 Pairwise Cipher Suites (next two lines)
        b'\x00\x0f\xac\x04'      # AES Cipher
        b'\x00\x0f\xac\x02'      # TKIP Cipher
        b'\x01\x00'              # 1 Authentication Key Managment Suite (line below)
        b'\x00\x0f\xac\x02'      # Pre-Shared Key
        b'\x00\x00'              # RSN Capabilities (no extra capabilities)
    ))

    frame = RadioTap()/dot11/beacon/essid/rsn
    # frame.show()
    # hexdump(frame)
    # input()
    frames.append(frame)

# get 1000 different orderings of the 101 frames (so we have ~100k frames)
# we are appending, so delete the file before re-running this script
for i in range(1000):
    print(i)
    curr = random.sample(frames, len(frames))
    wrpcap(OFILE, curr, append=True)

print('done')

