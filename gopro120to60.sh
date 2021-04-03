SRC=$1
DST=$2

ffmpeg -i $SRC  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
ffmpeg -fflags +genpts -r 60  -y -i raw.h265 -c:v copy $DST
rm  raw.h265