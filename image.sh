# Convert image to 3-second 2160p60 video

SRC=$1 #folder
for f in $1/*.mp4
do
    DST=$(dirname $f)/$(basename $f| cut -d. -f1)-video.mp4
    ffmpeg -y -loop 1 -i $f -c:v libx265 -t 3 -pix_fmt yuv420p -vf scale=3840:2160 -framerate 60 $DST
done
