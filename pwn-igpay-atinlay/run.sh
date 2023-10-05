#!/bin/bash
set -e
./build.sh
docker run --rm --privileged -p 1337:5000 -it igpay-atinlay-natoriay-3000
