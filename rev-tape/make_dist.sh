#!/bin/sh

rm -rf dist/
mkdir -p dist/

cd belt/

cargo build --release

cp target/release/belt ../dist/

cd ..

python3 make_flag_checker.py > flag_checker.blt

python3 ass.py flag_checker.blt flag_checker

mv flag_checker dist/

zip -r dist.zip dist/