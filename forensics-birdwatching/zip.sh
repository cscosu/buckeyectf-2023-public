#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp images/* "$temp_dir"
cp dist.README.md "$temp_dir"/README.md

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
