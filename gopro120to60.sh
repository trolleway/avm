
# convert 120fps to 60fps for h265
# $3 - start time
# $4 - duration time

SRC=$1
DST=$2



if [ ! -z $3 ] 
then 
    ffmpeg -hide_banner -loglevel error -i $SRC  -ss $3 -t $4  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r 60  -y -i raw.h265 -c:v copy $DST
	rm  raw.h265
else
    ffmpeg -hide_banner -loglevel error -i $SRC  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r 60  -y -i raw.h265 -c:v copy $DST
	rm  raw.h265
fi

