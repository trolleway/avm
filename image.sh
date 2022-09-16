# Convert image to 3-second 2160p60 video

SRC=$1 #folder
for f in $1/*.jpg $1/*.png
do
    DST=$(dirname $f)/$(basename $f| cut -d. -f1)-video.tmp.mp4
   echo ffmpeg  -hide_banner -loglevel error -y -loop 1 -i $f -c:v libx265 \
-t 3 -pix_fmt yuv420p \
-vf \
"scale=w=3840:h=2160:force_original_aspect_ratio=disable, \
fps=60" \
-framerate 60  \
$DST

SRC2=$DST
DST2=$(dirname $f)/$(basename $f| cut -d. -f1)-video.mp4

echo ffmpeg  -hide_banner -loglevel error -y -i anullsrc=channel_layout=stereo:sample_rate=44100 -i $SRC2 \
-vf "fade=t=in:st=0:d=0.5,fade=t=out:st=2.5:d=0.5"  -c:a aac -shortest  $DST2
rm -rf $SRC2
done
##-vf "fade=t=out:st=2.5:d=0.5" \
