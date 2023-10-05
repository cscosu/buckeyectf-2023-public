#!/usr/bin/env bash

set -x

temp_dir=$(mktemp -d)
trap "rm -r $temp_dir" EXIT

cp .eslintrc.json "$temp_dir"
cp .gitignore "$temp_dir"
cp next.config.js "$temp_dir"
cp package.json "$temp_dir"
cp pnpm-lock.yaml "$temp_dir"
cp postcss.config.js "$temp_dir"
cp prettier.config.cjs "$temp_dir"
cp tailwind.config.ts "$temp_dir"
cp tsconfig.json "$temp_dir"
cp docker-compose.yaml "$temp_dir"
cp dist.Dockerfile "$temp_dir"/Dockerfile
cp dist.entrypoint.sh "$temp_dir"/entrypoint.sh
cp dist.README.md "$temp_dir"/README.md
cp -r src "$temp_dir"/src
cp -r public "$temp_dir"/public

mkdir -p "$temp_dir"/flag
echo "bctf{fake_flag}" > "$temp_dir"/flag/index.html

out=$(pwd)
cd "$temp_dir"
zip -r "export.zip" .
mv "export.zip" "$out"/export.zip
