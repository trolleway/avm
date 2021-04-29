# Convert image to 3-second 2160p60 video

SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-video.mp4
ffmpeg -y -loop 1 -i SRC -c:v libx265 -t 3 -pix_fmt yuv420p -vf scale=3840:2160 -framerate 60 $DST
