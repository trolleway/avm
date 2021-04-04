
# convert to h264 for preview

SRC=$1
DST=$2

ffmpeg -i $SRC -y -vf scale=1280:720 -c:v libx264  -crf 30 -preset ultrafast -c:a copy $DST

