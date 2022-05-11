
SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-twitter.mp4
ffmpeg -i $SRC -y -vf scale=1920:1080 -c:v libx264  -crf 19 -preset fast -c:a copy $DST

# -vf scale=-1:1080
