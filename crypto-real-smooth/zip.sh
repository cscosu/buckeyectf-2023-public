#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp dist.gitignore "$temp_dir"/.gitignore
cp dist.README.md "$temp_dir"/README.md
cp database.txt "$temp_dir"
cp main.py "$temp_dir"

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
