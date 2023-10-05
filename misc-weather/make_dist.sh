#!/bin/sh

python scripts/same.py --input-flag-file ./data/flag.txt --output-bitflip-file ./data/bitflip.txt --output-start-sound-file ./data/start.wav --output-end-sound-file ./data/end.wav
sox data/start.wav data/Tom.wav data/end.wav data/weather-before-audacity.wav
echo "edit data/weather-before-audacity.wav according to the admin instructions, then export to dist/weather.wav"
echo "or just copy it directly, I'm not the police"
