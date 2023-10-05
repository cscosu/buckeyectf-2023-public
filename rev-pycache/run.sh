#!/bin/bash
set -e
./build.sh
docker run --rm -p 5000:8000 -it skribl
