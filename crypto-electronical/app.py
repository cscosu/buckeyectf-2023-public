from Crypto.Cipher import AES
from flask import Flask, request, abort, send_file
import math
import os

app = Flask(__name__)

key = os.urandom(32)
flag = os.environ.get('FLAG', 'bctf{fake_flag_fake_flag_fake_flag_fake_flag}')

cipher = AES.new(key, AES.MODE_ECB)

def encrypt(message: str) -> bytes:
    length = math.ceil(len(message) / 16) * 16
    padded = message.encode().ljust(length, b'\0')
    return cipher.encrypt(padded)

@app.get('/encrypt')
def handle_encrypt():
    param = request.args.get('message')

    if not param:
        return abort(400, "Bad")
    if not isinstance(param, str):
        return abort(400, "Bad")

    return encrypt(param + flag).hex()

@app.get('/source')
def handle_source():
    return send_file(__file__, "text/plain")

@app.get('/')
def handle_home():
    return """
        <style>
            form {
                display: flex;
                flex-direction: column;
                max-width: 20em;
                gap: .5em;
            }

            input {
                padding: .4em;
            }
        </style>
        <form action="/encrypt">
            <h2><i>ELECTRONICAL</i></h2>
            <label for="message">Message to encrypt:</label>
            <input id="message" name="message"></label>
            <input type="submit" value="Submit">
            <a href="/source">Source code</a>
        </form>
    """

if __name__ == "__main__":
    app.run()