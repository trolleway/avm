
SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-twitter.mp4
ffmpeg -i $SRC -y -vf scale=1920:1080 -c:v libx264  -crf 24 -preset fast -c:a copy $DST

# -vf scale=-1:1080


# wget -O- https://domain/file.mp4 | ffmpeg -i -
# time wget -O- https://upload.wikimedia.org/wikipedia/commons/5/5f/Saint_Petersburg_tram_1313_2007-09_1191099600_Lensoveta_Street_LM-99AV.webm | ffmpeg -i - -y  -c:v libx264  -crf 24 -preset fast -c:a libmp3lame twitter.mp4