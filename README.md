# avm
avm for Android Video Montage. 

Montage in a bash.

Toolset for ffmpeg faster 2160p60 h265 video editing on Android/Termux/Docker for sharing

# Usage

1. Install and run Termux
2. pkg in git -y
3. git clone https://github.com/trolleway/avm.git
4. termux-setup-storage 

Run scripts in termux default folder,
process files in android filesystem.

# Examples


### Start docker with ffmpeg interactive (bash or PowerShell) 
docker run -it  --entrypoint='bash'  -v ${PWD}:/tmp/workdir  jrottenberg/ffmpeg  

--- slow down gopro 120 fps to 60 fps with optional clip
./avm/gopro120to60.sh opolchenie/20210402-07.MP4  opolchenie/stage/20210402-07.MP4
./avm/gopro120to60.sh opolchenie/20210402-10.MP4  opolchenie/stage/20210402-10.MP4 1 3

---- convert any gopro h264 video to 60 fps 
./avm/goproh264to60.sh GH016403.MP4  res/ramenskiy-boolvar.MP4 60 66


ffmpeg -y -i opolchenie/stage/20210402-50.MP4 -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k  opolchenie/stage/20210402-50-h265.MP4 
rm

--- merge h265 videos withouth re-encoding
./avm/merge.sh opolchenie
----
gp120to60hevc
ffmpeg -i 20210402-05.MP4  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
ffmpeg -fflags +genpts -r 60  -y -i raw.h265 -c:v copy stage/20210402-05-265.MP4
rm  raw.h265

---- encoding for instagram (crop to square)
time ffmpeg -y -i opolchenie/stage/export/merge.MP4 -vf crop=1080:1080:812:220 -framerate 30 opolchenie/stage/export/merge-instagram.MP4
time ffmpeg -y -i mnevniki/stage/export/merge-audio.MP4 -vf crop=1080:1080:812:220 -framerate 30 mnevniki/stage/export/merge-audio-instagram.MP4
----- encoding for twitter
./avm/enc-twitter.sh opolchenie/stage/export/merge.MP4  opolchenie/stage/export/merge-twitter.MP4

./avm/gopro120to60.sh opolchenie/20210402-07.MP4  opolchenie/stage/20210402-07.MP4

