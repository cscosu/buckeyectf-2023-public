#!/bin/sh

rm -r dist
mkdir dist

./scripts/gen-l33t-names.py ./data/names-nonl33t.txt ./data/names-l33t.txt
./scripts/gen-frames.py ./data/names-l33t.txt ./data/flag.txt ./dist/frames.pcap

