#merge mp4 files (h264 or 265) withouth encoding

SRC=$1 #folder
DST=$SRC/merge
DATE=$(date +%Y-%m-%d)

#create dir if not exists
mkdir -p  $DST
#convert to mpeg transport stream
for f in $1/*.[mM][pPKk][4vV]; do ffmpeg -y  -hide_banner -loglevel error -i $f -c copy  -f mpegts $DST/$(basename $f| cut -d. -f1).ts; done
LIST='concat:'
for f in $DST/*.ts; do LIST+="$f|" ; done
#merge
ffmpeg -y  -hide_banner -loglevel error -i "$LIST" -c copy -bsf:a aac_adtstoasc $DST/$DATE.mp4

rm -rf $DST/*.ts
rm -rf $DST/list.txt
