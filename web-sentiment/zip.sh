#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp .gitignore "$temp_dir"
cp server.tsx "$temp_dir"
cp default.md "$temp_dir"
cp docker-compose.yaml "$temp_dir"
cp bun.lockb "$temp_dir"
cp Dockerfile "$temp_dir"
cp package.json "$temp_dir"
cp styles.css "$temp_dir"
cp tsconfig.json "$temp_dir"
cp dist.README.md "$temp_dir"/README.md

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
