#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp buckeyectf-2023-logo.png "$temp_dir"
cp bun.lockb "$temp_dir"
cp discord-screenshot.png "$temp_dir"
cp dist.gitignore "$temp_dir"/.gitignore
cp dist.README.md "$temp_dir"/README.md
cp docker-compose.yaml "$temp_dir"
cp Dockerfile "$temp_dir"
cp index.html "$temp_dir"
cp package.json "$temp_dir"
cp public_key.pem "$temp_dir"/remote_public_key.pem
cp server.tsx "$temp_dir"
cp tsconfig.json "$temp_dir"

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
