rm -rf dist/ dist.zip

mkdir -p dist/

cp chal.c Dockerfile make-capstone.sh build.sh run.sh dist/

zip -r dist.zip dist/
