# `misc-pong`

Sending an ICMP Echo Response will elicit a reply with a chunk of data appended to the reply according to the sequence number. Seq=0 is first chunk, etc. This makes a png with the flag. The PNG magic bytes in seq 0 data chunk should make the solution obvious.

Ideally we give the user an ip that is pingable with no other open services.

I made `build.dockerfile` because I dont want the github action to deploy my challenge.

## Solving

During the CTF a couple people didn't like that the file was so long because it took a long time to get the file.

Also if you have unstable/slow internet then it will take a long time.

However this is not the case.

I made the file large so that participants couldn't just run ping to get the flag in a reasonable time.

In `solve2.py` I add 100ms of latency and drop 25% of the packets it takes 11 seconds.

Even with 500ms of latency and dopping 50% of the packets it takes just 70 seconds.

Note: You have to `pip3 install -e icmplib`. I added an option to get the returned data from icmplib.

## Flag

bctf{pL3a$3_$t0p_p1nG1ng_M3}
