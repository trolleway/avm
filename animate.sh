#animate folder on png frames to h265 video

SRC=$1 #folder
DST=$SRC/animated
DATE=$(date +%Y-%m-%d)

#create dir if not exists


ffmpeg -framerate 60 -pattern_type glob -i $SRC/'*.png' \
  -c:v libx265 -pix_fmt yuv420p $SRC-animated.mp4