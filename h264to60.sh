
# convert 120fps to 60fps for h264
# $2 - start time
# $3 - duration time

SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-60fps.mp4



if [ ! -z $2 ] 
then 
    ffmpeg -i $SRC  -ss $2 -t $3  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r 60  -y -i raw.h264 -c:v copy $DST
	rm  raw.h264
else
    ffmpeg -i $SRC  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r 60  -y -i raw.h264 -c:v copy $DST
	rm  raw.h264
fi

