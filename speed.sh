
SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-speed.mp4
ffmpeg -i $SRC -y -vf "setpts=0.1*PTS" $DST
