#!/bin/sh

set -e

ver=$(python3 --version)
if [[ ! "$ver" == *"3.13"* ]]
then
    echo "Please run with python 3.13"
    exit 1
fi


DIST=dist/
CHAL=chal/

rm -rf $DIST dist.zip
mkdir -p $DIST
cp -r $CHAL $DIST

cd $DIST/chal
rm -rf __pycache__/

FLAG="bctf{fake_flag}" flask --app skribl.py run &
pid=$!
sleep 1

kill $pid

rm backend.py

cd ../..

cp Dockerfile $DIST
zip -r dist.zip $DIST