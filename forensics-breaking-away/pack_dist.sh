#!/usr/bin/env sh

rm -rf dist
mkdir dist

cp pdf/out.pdf dist/breaking-away.pdf

cd dist
zip -r dist.zip .
mv dist.zip ..
cd ..
rm -rf dist
mkdir dist
name=${PWD##*/}
mv dist.zip dist/$name.zip