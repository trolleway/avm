#merge mp4 files (h264 or 265) withouth encoding

SRC=$1 #folder
DST=$2 #folder

#create dir if not exists
mkdir -p  $DST
#convert to mpeg transport stream
for f in $1/*.MP4; do ffmpeg -y  -hide_banner -loglevel error -i $f -c copy  -f mpegts $DST/$(basename $f| cut -d. -f1).ts; done
LIST='concat:'
for f in $2/*.ts; do LIST+="$f|" ; done
#merge
ffmpeg -y  -hide_banner -loglevel error -i "$LIST" -c copy -bsf:a aac_adtstoasc $2/merge.MP4

rm -rf $2/*.ts
rm -rf $2/list.txt