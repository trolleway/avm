
# convert 120fps to 60fps for h265
# $2 - start time
# $3 - duration time

SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-60fps.MP4



if [ ! -z $2 ] 
then 
    ffmpeg -hide_banner -loglevel error -i $SRC  -ss $2 -t $3  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r 60  -y -i raw.h265 -c:v copy $DST
	rm  raw.h265
else
    ffmpeg -hide_banner -loglevel error -i $SRC  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r 60  -y -i raw.h265 -c:v copy $DST
	rm  raw.h265
fi

