FROM debian:bookworm-slim@sha256:24c92a69df28b21676d721fe18c0bf64138bfc69b486746ad935b49cc31b0b91 as build

RUN apt update -y && apt upgrade -y && \
    apt-get install -y build-essential

WORKDIR /app

COPY beginner-menu.c makefile flag.txt ./

RUN make menu && \
    mv menu run


FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c as prod

COPY --from=build / /srv
