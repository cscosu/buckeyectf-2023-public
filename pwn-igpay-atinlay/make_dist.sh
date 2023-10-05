#!/bin/sh

rm -rf dist/ dist.zip

mkdir -p dist/

cp -r chal/ dist/

rm -r dist/chal/target

cp Dockerfile dist/

zip -r dist.zip dist/