
# convert fps with change duration, no recompress
# $2 - fps

SRC=$1
FPS=$2
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-$2-fps.MP4



ffmpeg -i $SRC  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
ffmpeg -fflags +genpts -r $2  -y -i raw.h264 -c:v copy $DST
rm  raw.h264

