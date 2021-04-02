SRC=$1
DST=$2
ffmpeg -i $SRC -y  -vf scale=720:-1 -c:v libx264 -crf 18 -preset veryslow -c:a copy $DST
