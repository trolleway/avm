
SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-twitter.mp4
ffmpeg -i $SRC -y -vf scale=1920:1080 -c:v libx264 -hide_banner -tune film -crf 19 -preset medium -c:a copy $DST


DST=$(dirname $1)/$(basename $1| cut -d. -f1)-instagram.mp4
ffmpeg -i $SRC -y -vf crop=2160:2160:653:0  -vf scale=1920:1080 -c:v libx264  -framerate 30  -crf 19 -preset faster -c:a copy $DST
