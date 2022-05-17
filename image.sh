# Convert image to 3-second 2160p60 video

SRC=$1 #folder
for f in $1/*.jpg $1/*.png
do
    DST=$(dirname $f)/$(basename $f| cut -d. -f1)-video.mp4
    ffmpeg -y -loop 1 -i $f -c:v libx265 \
-t 3 -pix_fmt yuv420p \
-vf scale=w=3840:h=2160:force_original_aspect_ratio=disable \
-framerate 60 -filter:v fps=60 \
-vf "fade=t=out:st=2.5:d=0.5" \
$DST
done
