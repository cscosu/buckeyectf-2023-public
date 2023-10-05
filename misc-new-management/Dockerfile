FROM node:20-alpine AS js-stage

COPY contracts /contracts
WORKDIR /contracts
COPY .env .env
RUN npm install -g truffle && npm install
RUN mkdir temp && cp -r migrations contracts truffle-config.js temp/
RUN truffle init && rm -rf ./contracts ./migrations truffle-config.js && mv temp/* . && truffle compile
RUN truffle migrate --network sepolia

FROM python:3.10-slim
COPY app /app
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache --upgrade setuptools wheel
WORKDIR /app
RUN pip install -r requirements.txt
COPY .env .env
COPY --from=js-stage /contracts/build/contracts/NewManagement.json /app/

WORKDIR /
COPY start.sh start.sh
EXPOSE 1337
ENTRYPOINT ["sh", "start.sh"]