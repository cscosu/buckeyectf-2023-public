FROM rust:slim@sha256:ff798ceb500fa43c91db10db881066057fefd36e16d531e7b1ed228ab2246175     as build

RUN rustup target add x86_64-unknown-linux-musl 

WORKDIR /app
COPY pong/ /app

RUN cargo build --release --target x86_64-unknown-linux-musl

RUN cp target/x86_64-unknown-linux-musl/release/pong ./pong && \
    chmod 755 ./pong

FROM alpine:latest@sha256:7144f7bab3d4c2648d7e59409f15ec52a18006a128c733fcff20d3a4a54ba44a as prod

WORKDIR /app
COPY flag.png /app/
COPY --from=build /app/pong /app/pong

RUN apk add --no-cache tini
# Enable ctrl-c
ENTRYPOINT ["/sbin/tini", "--"]
CMD [ "/app/pong" ]