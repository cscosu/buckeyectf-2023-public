import pwn
import ast
import copy
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_pem_public_key,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import struct
from util import *
from proof import *
import random

pwn.context.log_level = "debug"

if pwn.args.REMOTE:
    io = pwn.remote("chall.pwnoh.io", 13396)
else:
    io = pwn.process("python3 ../main.py", shell=True)

io.recvuntil(b"Alice's public key is ")
alice_public_key_bytes = bytes.fromhex(io.readline().decode())
alice_public_key = load_pem_public_key(alice_public_key_bytes)

io.recvuntil(b"Bob's authentication path was:\n")
t = io.readline().decode()
bob_ap = ast.literal_eval(t)

level = int(bob_ap["leaf"]["level"])
bob_index = hashlib.sha256(b"bob").digest()
bob_prefix_bits = bytes_to_bits(bob_index)

while True:
    username = "bob" + random.randbytes(4).hex()
    index = hashlib.sha256(username.encode()).digest()
    index_bits = bytes_to_bits(index)
    if index_bits[:level] == bob_prefix_bits[:level]:
        break

io.sendlineafter(b"Enter your username: ", username)

private_key = ec.generate_private_key(ec.SECP256R1())
public_key_bytes = private_key.public_key().public_bytes(
    Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
)

io.sendlineafter(b"Enter your public key in hex: ", public_key_bytes.hex())
io.sendlineafter(b"Please specify a username: ", username)

io.recvuntil(b"Ciphertext: ")
ct = bytes.fromhex(io.readline().decode())

io.recvuntil(b"IV: ")
iv = bytes.fromhex(io.readline().decode())

shared_key = private_key.exchange(ec.ECDH(), alice_public_key)  # type: ignore
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=None,
).derive(shared_key)

cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
decryptor = cipher.decryptor()
print(decryptor.update(ct) + decryptor.finalize())
