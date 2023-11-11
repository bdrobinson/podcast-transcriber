#!/bin/sh

set -e

URL=$1
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S%z")
OUTPUT_DIR=/output/$TIMESTAMP

mkdir -p $OUTPUT_DIR

echo "Downloading $URL"
curl -Ls -o ./audio.mp3 $URL
echo "Downloaded! Now running whisper..."
whisper audio.mp3 --model tiny.en -o $OUTPUT_DIR