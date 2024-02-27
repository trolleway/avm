
# convert to h264 for preview

SRC=$1
DST=$2
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-preview.mp4

ffmpeg -i $SRC -y -vf scale=-2:'min(720,ih)' -c:v libx264  -crf 31 -preset ultrafast -vf "drawtext=fontfile=Jura.ttf: timecode='00\:00\:00\:00':r=30:x=10:y=10:fontsize=140:fontcolor=gray" -c:a aac -b:a 160k -movflags +faststart $DST

