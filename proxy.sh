# Convert image to 3-second 2160p60 video

SRC=$1 #folder
DSTDIR=$SRC/proxy/
mkdir $DSTDIR

for f in $1/*.mp4 $1/*.MP4
do
    DST=$(dirname $f)/proxy/$(basename $f)
	if test -f "$DST"; then
		echo "$DST exists."
		continue
	fi
	echo $DST


    ffmpeg  -hide_banner -loglevel error -i $f -y -vf scale=1280:720 -c:v libx264  -crf 30 -preset ultrafast -c:a copy $DST


done
##-vf "fade=t=out:st=2.5:d=0.5" \
