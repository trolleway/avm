# Convert image to 3-second 2160p60 video

SRC=$1 #folder
for f in $1/*.jpg
do
    DST=$(dirname $f)/$(basename $f| cut -d. -f1)-video.mp4
    ffmpeg -y -loop 1 -i $f -c:v libx265 \
-t 6 -pix_fmt yuv420p \
-vf scale=w=3840:h=2160:force_original_aspect_ratio=disable \
 -framerate 60 $DST
done
