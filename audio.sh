SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-audio.mp4

ffmpeg -i $SRC -i $2 -y -c:v copy -map 0:v -map 1:a -c:v copy -shortest  $DST
