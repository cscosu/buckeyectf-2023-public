from ubuntu:22.04

RUN apt update && apt upgrade -y
RUN apt install vim sudo gcc-arm-linux-gnueabi qemu-user gdb-multiarch make -y

