FROM ubuntu:jammy-20230816 AS app
RUN apt-get update && apt-get install -y gcc make

WORKDIR /app
COPY Makefile maze.c run.sh ./
RUN make

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c
COPY --from=app / /srv
RUN chmod +x /srv/app/run.sh
RUN mv /srv/app/run.sh /srv/app/run