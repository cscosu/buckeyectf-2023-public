#!/usr/bin/env python

from itertools import product
import random
import sys

if len(sys.argv) < 3:
    print('needs args')
    exit(1)

IFILE = sys.argv[1]
OFILE = sys.argv[2]
LEET = {
    'a': '4',
    'e': '3',
    'g': '6',
    'l': '1',
    'o': '0',
    's': '5',
    't': '7',
}


with open(IFILE, 'r') as inf:
    prenames = inf.readlines()

postnames = []

# https://stackoverflow.com/questions/29151145/how-can-i-get-all-possible-leet-versions-of-a-string-with-optional-substituti
for name in prenames:
    varieties = [
        ''.join(letters) for letters in product(
            *(
                {c, LEET.get(c, c)} for c in name
            )
        )
    ]
    # print(varieties)
    # print(len(varieties))
    # input()
    selected = random.sample(varieties, 10)
    postnames += selected

with open(OFILE, 'w') as outf:
    outf.writelines(postnames)

print('done')

