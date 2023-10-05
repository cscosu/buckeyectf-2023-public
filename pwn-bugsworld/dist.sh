#!/usr/bin/env bash
mkdir dist
cp bugsworld bugsworld.c Makefile Dockerfile docker-compose.yml dist
echo bctf{fake_flag} > dist/flag.txt
cp readme.dist.md dist/readme.md
cd dist
zip -r ../export.zip .
cd ..
rm -r dist