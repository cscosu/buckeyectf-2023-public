#!/usr/bin/env bash
mkdir dist
cp flag.compressed dist/
cp -r info dist/
cd dist
zip -r ../dist.zip .
cd ..
rm -r dist
