#/usr/bin/env bash

mkdir -p dist/{client,server}
cp ./types.ts dist
cp ./client/index.html ./client/package.json ./client/pnpm-lock.yaml \
    ./client/postcss.config.js ./client/tailwind.config.js ./client/tsconfig.json \
    ./client/tsconfig.node.json ./client/vite.config.ts ./dist/client
cp -r ./client/src/ ./dist/client/src/
cp ./server/package.json ./server/pnpm-lock.yaml ./server/app.ts ./server/tsconfig.json ./dist/server
cp ./Dockerfile ./docker-compose.yml ./dist

cd dist
zip -r ../export.zip .
cd ..
rm -r dist