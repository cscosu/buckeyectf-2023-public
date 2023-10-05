#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp .gitignore "$temp_dir"
cp app.ts "$temp_dir"
cp bun.lockb "$temp_dir"
cp Dockerfile "$temp_dir"
cp package.json "$temp_dir"
cp supervisord.conf "$temp_dir"
cp tsconfig.json "$temp_dir"
cp docker-compose.yaml "$temp_dir"
cp dist.README.md "$temp_dir"/README.md

mkdir -p "$temp_dir"/flag
echo "bctf{fake_flag}" > "$temp_dir"/flag.txt

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
