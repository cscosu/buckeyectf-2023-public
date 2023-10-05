#!/usr/bin/env bash
mkdir dist
cp app.mjs docker-compose.yml Dockerfile package.json package-lock.json dist
cd dist
zip -r ../export.zip .
cd ..
rm -r dist