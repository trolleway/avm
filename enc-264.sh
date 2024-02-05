SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-h264.mp4
ffmpeg -i $SRC -hide_banner -y -c:v libx264  -crf 19 -preset slow -tune film -c:a aac $DST
