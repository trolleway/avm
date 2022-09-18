
# convert to h264 for preview

SRC=$1


ffplay -i $SRC -vf scale=1280:720

