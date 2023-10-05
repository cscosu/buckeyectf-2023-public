#!/usr/bin/env bash
mkdir dist
cp flag.compressed dist/
cd dist
zip -r ../dist.zip .
cd ..
rm -r dist
