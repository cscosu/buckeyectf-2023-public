#!/bin/sh

set -e

python3 ass.py $1 out
cd belt
cargo run ../out
cd ..