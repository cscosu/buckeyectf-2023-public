mkdir dist
cp index.html index.ts Dockerfile docker-compose.yml dist
echo bctf{fake_flag} > dist/flag.txt
cd dist
zip -rq ../export.zip .
cd ..
rm -r dist