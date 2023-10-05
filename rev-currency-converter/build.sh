 
rm -rf build/
mkdir -p build

javac -d ./build *.java

cd build

jar cfe converter.jar main main.class CurrencyConverter.class

cd ..

