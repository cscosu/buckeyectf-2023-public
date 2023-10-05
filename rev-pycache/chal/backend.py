import string
import random
import time
import math
import os


def create_skribl(skribls, message, author) -> str:
    print(f"Creating skribl {message}")

    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    key_list = [random.choice(alphabet) for i in range(40)]

    key = ''.join(key_list)
    skribls[key] = (message, author)
    return key

def init_backend(skribls):
    random.seed(math.floor(time.time()))

    create_skribl(skribls, os.environ['FLAG'], "rene")
