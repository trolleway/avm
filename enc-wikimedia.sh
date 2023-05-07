#/bin/bash
# Convert video file to webm for Wikimedia Commons
# Author: 
# Parameters:
#  P1: input file name

if [[ -z "$1" ]] ;then echo "Input file missing" ;exit ;fi

input="$1"
output=$(basename "$1").webm

echo "Frames count:"
framecount.sh $input

ffmpeg -i "$input" -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 1 -row-mt 1 -an -f webm -y /dev/null && ffmpeg -i "$input" -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 2 -row-mt 1 -c:a libopus "$output"
