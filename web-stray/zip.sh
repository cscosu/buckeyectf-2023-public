#!/usr/bin/env bash

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp .gitignore "$temp_dir"
cp app.js "$temp_dir"
cp dist.README.md "$temp_dir"/README.md
cp docker-compose.yaml "$temp_dir"
cp Dockerfile "$temp_dir"
cp index.html "$temp_dir"
cp package.json "$temp_dir"
cp pnpm-lock.yaml "$temp_dir"
cp -r names "$temp_dir"

echo "bctf{fake_flag}" > "$temp_dir"/flag.txt

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
