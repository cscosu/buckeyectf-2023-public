FROM node:lts AS runtime
WORKDIR /app

RUN npm install -g pnpm

COPY package.json .
COPY pnpm-lock.yaml .
COPY .env .
COPY prisma/schema.prisma prisma/schema.prisma

RUN pnpm install
RUN pnpm prisma db push

COPY public public
COPY src src
COPY template template
COPY next.config.mjs .
COPY postcss.config.cjs .
COPY tailwind.config.ts .
COPY tsconfig.json .

RUN pnpm build

ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0
EXPOSE 3000
CMD pnpm start
