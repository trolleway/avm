
# convert 120fps to 60fps for h265
# $3 - start time
# $4 - duration time

SRC=$1
DST=$2



if [ ! -z $3 ] 
then 
    ffmpeg -i $SRC  -ss $3 -t $4  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r 60  -y -i raw.h264 -c:v copy $DST
	rm  raw.h264
else
    ffmpeg -i $SRC  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r 60  -y -i raw.h264 -c:v copy $DST
	rm  raw.h264
fi

