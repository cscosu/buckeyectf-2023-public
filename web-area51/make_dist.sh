echo Making dist.zip

rm -rf dist dist.zip

mkdir -p dist

cp -r area51/ dist/
rm -rf dist/area51/node_modules/

cp Dockerfile entrypoint.sh init_users.js wait_for_mongo.js dist/

zip -r dist.zip dist/