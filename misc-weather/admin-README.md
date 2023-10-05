## About
Author: `arcsolstice`

Tags: `misc` `networking`

Difficulty: `medium`

## Public Description
Use the meme.jpg in this folder. If including an image in the challenge description isn't possible, use the following text:
"A flag warning?! At this time of year, at this time of day, in this part of the country, entirely localized within a single CTF competition?"

## Files to Distribute
`weather.wav` from the `dist` folder

## Admin Notes
- we give them a wav audio file with 16-bit signed samples at 44.1khz
- the python script generates the start and end of the audio track automatically
    - the python script involves some randomness, so the output won't be the exact same every time
- the middle of the audio track is generated using the same (I think) TTS that the National Weather Service used until 2016. getting that TTS program working was sorta cursed and involved downloading a Windows Server 2003 VM disk image from a google drive link in a youtube video description, so not everything needed to generate it is included here, lol
- `make_dist.sh` combines the wav files (assuming they are all mono and same # of channels) into a single file. I thought it sounded too "clean" at this point, so I made some changes in audacity that you would have to replicate manually if you were re-generating the output:
    - Track -> new
    - Generate -> Noise -> White, 0.1 (on the new track)
    - Effect -> EQ and Filters -> Filter Curve EQ, AM Radio preset (on both tracks)
    - Effect -> Volume and Compression -> Amplify, new peak amplitude -3.0db (on the weather track only, not the noise track)
- the final export (signed 16 bit, wav) from audacity should then be roughly the same as the one that comes in the dist folder with this git repo

## Expected Solve
- Option A:
    - From context and googling, realize the audio is an EAS warning with SAME-encoded data
    - **Download a decoder from github**
    - Decode each of the 3 initial bursts. Realize each is the flag BUT with some noise injected
    - Use the columnar-parity-based error correction scheme detailed by the SAME specification to recover the uncorrupted flag bits
- Option B:
    - From context and googling, realize the audio is an EAS warning with SAME-encoded data
    - **Read the spec and write your own tooling to decode the data (e.g. GnuRadio, numpy)**
    - Decode each of the 3 initial bursts. Realize each is the flag BUT with some noise injected
    - Use the columnar-parity-based error correction scheme detailed by the SAME specification to recover the uncorrupted flag bits

