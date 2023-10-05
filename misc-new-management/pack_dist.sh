#!/usr/bin/env sh

rm -rf dist
mkdir dist

cp contracts/contracts/NewManagement.sol dist/

cd dist
zip -r dist.zip .
mv dist.zip ..
cd ..
rm -rf dist
mkdir dist
name=${PWD##*/}
mv dist.zip dist/$name.zip