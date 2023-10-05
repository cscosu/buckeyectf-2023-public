#!/usr/bin/env bash
make
mkdir dist
cp maze dist/
cd dist
zip -r ../dist.zip .
cd ..
rm -r dist
make clean
