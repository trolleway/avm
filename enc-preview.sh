
# convert to h264 for preview

SRC=$1
DST=$2
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-preview.mp4

ffmpeg -i $SRC -y -vf scale=1280:720 -c:v libx264  -crf 30 -preset ultrafast -c:a copy $DST

