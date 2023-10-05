import numpy as np
from scipy.io import wavfile
import random
import sys
import subprocess # to play the resulting wave file
import datetime # EAS alerts are heavily dependent on timestamps so this makes it easy to send a thing now
import argparse

import random

## ORIGINAL CREDIT https://github.com/nicksmadscience/eas-same-encoder ##

# parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--playaudiolive", "-pal", nargs='?', default=-1)
parser.add_argument("--code", "-c", nargs='?', default="none")
parser.add_argument("--input-flag-file", "-iff", required=True)
parser.add_argument("--output-bitflip-file", "-obf", required=True)
parser.add_argument("--output-start-sound-file", "-ossf", required=True)
parser.add_argument("--output-end-sound-file", "-oesf", required=True)
args = parser.parse_args()

print(args)

######## CONFIG / constants ########

markBitFrequency = 2083 + (1/3)
spaceBitFrequency = 1562.5
attentionFrequency = 1050

# sample rate
fs = 44100


def markBit():
    global markBitFrequency

    # f = 2083.33333
    f = markBitFrequency
    t = 1.0 / (520 + (5/6))
    
    samples = np.arange(t * fs) / fs

    roffle = np.sin(2 * np.pi * f * samples)
    # makes it easier to see by slightly modulating the amplitude
    # return roffle * 0.8
    return roffle

def spaceBit():
    global spaceBitFrequency

    # f = 1562.5
    f = spaceBitFrequency
    t = 1.0 / (520 + (5/6))
    
    samples = np.arange(t * fs) / fs

    return np.sin(2 * np.pi * f * samples)

def attentionTone():
    global attentionFrequency

    f = attentionFrequency
    t = 10.0

    samples = np.arange(t * fs) / fs

    return np.sin(2 * np.pi * f * samples)


# start with 1 second of silence each
start_signal    = np.zeros(fs)
end_signal      = np.zeros(fs)


def byte(the_byte):
    sys.stdout.write(the_byte)
    sys.stdout.write(" ")
    byte_data = np.zeros(0)
    for i in range(0, 8):
        if ord(the_byte) >> i & 1:
            sys.stdout.write("1")
            byte_data = np.append(byte_data, markBit())
        else:
            sys.stdout.write("0")
            byte_data = np.append(byte_data, spaceBit())

    sys.stdout.write("\n")
    sys.stdout.flush()

    return byte_data


def extramarks(numberOfMarks):
    """SAGE encoders seem to add a few mark bits at the beginning and end"""
    byte_data = np.zeros(0)

    for i in range(0, numberOfMarks):
        byte_data = np.append(byte_data, markBit())

    return byte_data

def preamble():
    byte_data = np.zeros(0)

    for i in range(0, 16):
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())
        byte_data = np.append(byte_data, spaceBit())
        byte_data = np.append(byte_data, markBit())



    return byte_data




# ZCZC-WXR-RWT-020103-020209-020091-020121-029047-029165-029095-029037+0030-1051700-KEAX/NWS

# code = "ZCZC-EAS-RMT-011000+0100-2141800-SCIENCE-"
# code = "ZCZC-WXR-TOR-000000+0030-2142200-SCIENCE -"
# code = "ZCZC-PEP-EAN-000000+0400-2142350-SCIENCE -"

# control string
# code = "ZCZC-EAS-RMT-011000+0100-2142200-KMMS FM -"

# useful FIPS codes
# 000000 - the whole fucking united states
# 024031 - silver spring, md / montgomery county
# 011001 - district of columbia

# EAS alerts are heavily dependent on timestamps so this makes it easy/fun to send a thing now
sameCompatibleTimestamp = datetime.datetime.now().strftime("%j%H%M")

# known good
# OH SHIT it's all time-dependent
# which i can now do since the time works on the box
#code = "ZCZC-PEP-EAN-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
# code = "ZCZC-PEP-EAT-000000+0400-" + sameCompatibleTimestamp + "-SCIENCE -"  # nuclear armageddon (or some other form of "we are all likely to die")
# code = "ZCZC-PEP-EAT-000000+0400-2142350-SCIENCE -"  # lol jk no nuclear armageddon
# code = "ZCZC-WXR-TOR-024031+0030-" + sameCompatibleTimestamp + "-SCIENCE -"  # tornado warning, silver spring, md
# code = "ZCZC-WXR-SVR-024031+0030-2142200-SCIENCE -"  # severe thunderstorm warning, silver spring, md
# code = "ZCZC-WXR-EVI-024031+0030-" + sameCompatibleTimestamp + "-SCIENCE -"  # evacuation immediate!!, silver spring, md
# code = "ZCZC-WXR-FFW-024031+0030-2150021-SCIENCE -"

# testing
# code = "ZCZC-CIV-LAE-024031+0030-2150022-SCIENCE -"
# code = "ZCZC-CIV-CDW-024031+0400-" + sameCompatibleTimestamp + "-SCIENCE -"
# code = "ZCZC-PEP-EAN-024031+0030-" + sameCompatibleTimestamp + "-SCIENCE -"

# code = "ZCZC-ROFL-WTF-012345+0000-YO WADDUP MOTHAFUCKAZ="

with open(args.input_flag_file, 'r') as iff:
    raw_flag = iff.read().splitlines()[0]

# pad with '#' until length is a multiple of 6
if len(raw_flag) % 6:
    pad_len = 6 - (len(raw_flag) % 6)
else:
    pad_len = 0
pad_flag = raw_flag + '='*pad_len
# intersperse '-' every 6 chars
split_flag = '-'.join( pad_flag[i:i+6] for i in range(0, len(pad_flag), 6) )

code = "ZCZC-OSU-FLG-" + split_flag + "+4800-2730000-KK7LHY"

print(code)

def flip_bit(char, idx):
    val = ord(char)
    val ^= (1 << (7 - idx))
    char = chr(val)
    return char

bitflip_code = [ list(code[:]), list(code[:]), list(code[:]) ]

RAND_PROB = 0.1

for i in range(8 * len(code)):
    if random.random() < RAND_PROB:
        # only flip 1 out of the 3 so that the best-2-of-3 columnar parity works
        which_tx = random.randint(0, 2)
        bitflip_code[which_tx][i // 8] = flip_bit(bitflip_code[which_tx][i // 8], i % 8)

tx_code = [ "".join(x) for x in bitflip_code ]

print(tx_code)

with open(args.output_bitflip_file, 'w') as obf:
    obf.write('\n'.join(tx_code))

# code = args.code



for i in range(0, 3):
    # signal = np.append(signal, extramarks(10))
    start_signal = np.append(start_signal, preamble())

    # turn each character into a sequence of sine waves
    # for char in code:
    for char in tx_code[i]:
        start_signal = np.append(start_signal, byte(char))

    # signal = np.append(signal, extramarks(6)) # ENDEC might not be as picky about this as I once thought

    start_signal = np.append(start_signal, np.zeros(fs)) # wait the requisite one second

start_signal = np.append(start_signal, attentionTone())
start_signal = np.append(start_signal, np.zeros(fs)) # wait the requisite one second



# EOM (3x)
for i in range(0, 3):
    # signal = np.append(signal, extramarks(10))
    end_signal = np.append(end_signal, preamble())

    for char in "NNNN": # NNNN = End Of Message
        end_signal = np.append(end_signal, byte(char))

    # signal = np.append(signal, extramarks(6))

    end_signal = np.append(end_signal, np.zeros(fs)) # wait the requisite one second

    

start_signal *= 32767
end_signal *= 32767

start_signal = np.int16(start_signal)
end_signal = np.int16(end_signal)

wavfile.write(args.output_start_sound_file, fs, start_signal)
wavfile.write(args.output_end_sound_file, fs, end_signal)


if args.playaudiolive == "1":
    subprocess.call(f"afplay {args.output_start_sound_file}", shell=True)


