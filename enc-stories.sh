
echo "convert video to vertical"
echo "usage:  ./enc-stories.sh path align[1,2,3,9]"

SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-stories.mp4

# -vf scale=-1:1080

POS=$2

#ffplay -filter:v "crop=ih/16*9:ih" ~/tmp/skot.mp4

case $POS in

  1)
    ffmpeg -stats -i "$SRC" -y -vf scale=1080:1920 -vf "crop=ih/16*9:ih:0:0" -c:v libx264  -crf 19 -preset fast "$DST"
    ;;

  2)
    ffmpeg -stats -i "$SRC" -y -vf scale=1080:1920 -vf "crop=ih/16*9:ih:iw/10" -c:v libx264  -crf 19 -preset fast  "$DST"
    ;;

  3)
    ffmpeg -stats -i "$SRC" -y -vf scale=1080:1920 -vf "crop=ih/16*9:ih" -c:v libx264  -crf 19 -preset fast  "$DST"
    ;;

  *)
    ffmpeg -stats -i "$SRC" -y -vf scale=1080:1920 -vf "crop=ih/16*9:ih" -c:v libx264  -crf 19 -preset fast "$DST"
    ;;

  9)
    ffmpeg -stats -i "$SRC" -y -vf scale=1080:1920 -vf "crop=ih/16*9:ih:iw" -c:v libx264  -crf 19 -preset fast  "$DST"
    ;;
esac
