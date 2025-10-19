#merge mp4 files (h264 or 265) withouth encoding

SRC=$1 #folder
DST=$SRC/merge
DATE=$(date +%Y-%m-%d)

#create dir if not exists
mkdir -p  $DST

# Set the path to the directory containing the MJPG AVI files
directory_path="/path/to/your/directory"

# Concatenate all MJPG AVI files in the directory

(for f in "$SRC"/*.[aAmM][vVoO][iIvV]; do echo "file '$f'"; done) > list.txt

#for f in "$SRC"/*.[aA][vV][iI]; do echo "file '$f'"; done
#ffmpeg -f concat -safe 0 -i <(for f in "$SRC"/*.[aA][vV][iI]; do echo "file '$f'"; done) -c copy $DST/$DATE_merge.avi
ffmpeg -f concat -safe 0 -i list.txt -c copy $DST/$DATE.avi
rm -f list.txt