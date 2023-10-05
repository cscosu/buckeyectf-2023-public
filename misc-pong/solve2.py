import icmplib
from time import sleep
import time
import sys
from multiprocessing.dummy import Pool as ThreadPool
import itertools
import random

# TO RUN:
# `pip3 install -e icmplib` 


MAX_SIZE = 10000000
SEGMENT_SIZE = 64
flag_data = bytearray(MAX_SIZE)

HOST = "18.191.205.48"
#host = "127.0.0.1"
OUT_FILE = "out.png"

def write_data(data_array, segment_num, segment_data):
    segment_byte = segment_num * SEGMENT_SIZE
    i = 0
    for byte_idx in range(segment_byte, segment_byte + len(segment_data)):
        data_array[byte_idx] = segment_data[i]
        i += 1

def do_stuff(data_array, from_idx, to_idx):
    sock = icmplib.ICMPv4Socket(privileged=False)
    current_sequence = from_idx
    while current_sequence < to_idx:
        request = icmplib.ICMPRequest(HOST, 0x1337, current_sequence, payload_size=0)
        sock.send(request)
        print(f"Getting {current_sequence}")
        try:
            reply = sock.receive(request, timeout=5)
            time.sleep(0.5)
            if random.choice([True, False]):
                print("Oopsie packet dropped")
                continue
        except icmplib.exceptions.TimeoutExceeded:
            print(f"Packet {current_sequence} timed out...")
            continue
        data_loc = 0x1C # offset into payload
        if len(reply._packet) <= data_loc:
            print(f"Packet {current_sequence} had no data...")
            break
        data = reply._packet[data_loc:]
        write_data(data_array, current_sequence, data)
        current_sequence += 1
            


if __name__ == "__main__":
    start_time = time.time()
    step = 10
    end = 10000 # Guess
    starts = list(range(0, end, step))
    ends = [x+step for x in starts]

    pool = ThreadPool(100)

    args = zip(itertools.repeat(flag_data), starts, ends)
    print(args)
    results = pool.starmap(do_stuff, args)
    pool.close()
    pool.join()

        
    with open(OUT_FILE, "wb") as f:
        f.write(flag_data)
    
    end_time = time.time()
    print(f"Took {end_time - start_time} seconds")


