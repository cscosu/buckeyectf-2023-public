#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp 3-stripped.hs "$temp_dir"/emotional-damage.hs
cp dist.README.md "$temp_dir"/README.md

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
