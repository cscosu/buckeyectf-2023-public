## About
Author: `arcsolstice`

Tags: `misc` `networking`

Difficulty: `easy`

## Public Description
none

## Files to Distribute
`frames.pcap` from the `dist` folder

## Admin Notes
- we give them a pcap with ~100,000 wifi beacons, all with base64-encoded network names (SSID)
- most of the SSID names (100) are just bogus text
- only 1 SSID name is flag format
- `./make_dist.sh` should generate the `frames.pcap` if something happens to it (or you need to change the flag format), but note that it won't be the EXACT same because it uses rand for shuffling the order

## Expected Solve
- Write a python script
- Iterate through all the packets, saving the unique SSID names to a set. When done, there should be 101 unique names
- Base64 decode each of them and grep for `bctf{`, there is only 1 SSID name that matches and it is the flag

