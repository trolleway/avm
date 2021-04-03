echo $1
echo $2

SRC=$1
DST=$2
ffmpeg -i $SRC -y  -vf scale=-1:1080 -c:v libx264 -crf 18 -preset veryslow -c:a copy $DST
