#!/usr/bin/env bash

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp Dockerfile "$temp_dir"
cp requirements.txt "$temp_dir"
cp server.py "$temp_dir"
cp docker-compose.yaml "$temp_dir"
cp dist.README.md "$temp_dir"/README.md

echo "bctf{fake_flag}" > "$temp_dir"/flag.txt

out=$(pwd)
cd "$temp_dir"
zip -rq "export.zip" .
mv "export.zip" "$out"/export.zip
