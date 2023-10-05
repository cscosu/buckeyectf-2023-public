FROM python:3.8-slim-buster

WORKDIR /app
RUN pip3 install pycryptodome flask
COPY app.py ./

CMD python3 -m flask run --host=0.0.0.0