FROM alpine AS build-frontend
WORKDIR /build
RUN apk add npm
RUN npm i -g pnpm
COPY pnpm-lock.yaml .
COPY package.json .
RUN pnpm i
COPY src src
COPY public public
COPY tsconfig.json .
COPY tsconfig.node.json .
COPY index.html .
RUN pnpm build

FROM alpine AS build-backend
WORKDIR /build
RUN apk add go
COPY main.go .
RUN CGO_ENABLED=0 go build main.go

FROM alpine
COPY --from=build-frontend /build/dist /dist
COPY --from=build-backend /build/main /main
CMD ["/main"]
