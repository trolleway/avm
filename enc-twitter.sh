echo $1
echo $2

SRC=$1
DST=$2
ffmpeg -i $SRC -y  -c:v libx264  -crf 18 -preset veryslow -c:a copy $DST

# -vf scale=-1:1080
