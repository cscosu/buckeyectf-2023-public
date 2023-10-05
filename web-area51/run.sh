#!/bin/bash
set -e
./build.sh
docker run --rm -p8080:80 -it area51
