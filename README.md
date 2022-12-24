# avm
avm for Android Video Montage. 

Montage in a bash.

Toolset for ffmpeg faster 2160p60 h265 video editing on Android/Termux/Docker for sharing

# Usage

## Windows, Linux, Mac

* Install and start docker, then
* Download this repository  https://github.com/trolleway/avm/archive/refs/heads/main.zip or
```
git clone https://github.com/trolleway/avm.git
```
* Run interactively docker image with ffmpeg (bash or PowerShell on Windows)
```
docker run -it --rm  --entrypoint='bash'  -v ${PWD}:/tmp/workdir  jrottenberg/ffmpeg  
```


## Android
Install and run Termux. Install in home catalog. 

```
pkg in git -y
git clone https://github.com/trolleway/avm.git
cd avm
./deploy.sh
```


Run scripts in termux default folder,
process files in android filesystem.

# Examples


#### merge h264 or h265 mp4 videos withouth re-encoding
```
./avm/merge.sh dir_with_mp4
```

#### slow down gopro 120 fps to 60 fps with optional clip
```
./avm/gopro120to60.sh opolchenie/20210402-07.MP4  opolchenie/stage/20210402-07.MP4
./avm/gopro120to60.sh opolchenie/20210402-10.MP4  opolchenie/stage/20210402-10.MP4 1 3
```

#### convert any gopro h264 video to 60 fps 
```
./avm/goproh264to60.sh GH016403.MP4  res/ramenskiy-boolvar.MP4 60 66
ffmpeg -y -i opolchenie/stage/20210402-50.MP4 -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k  opolchenie/stage/20210402-50-h265.MP4 
```


#### gopro 120 fps to 60fps  hevc
```
ffmpeg -i 20210402-05.MP4  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
ffmpeg -fflags +genpts -r 60  -y -i raw.h265 -c:v copy stage/20210402-05-265.MP4
rm  raw.h265
```

#### convert video for instagram (crop to square)
```
time ffmpeg -y -i opolchenie/stage/export/merge.MP4 -vf crop=1080:1080:812:220 -framerate 30 opolchenie/stage/export/merge-instagram.MP4
time ffmpeg -y -i mnevniki/stage/export/merge-audio.MP4 -vf crop=1080:1080:812:220 -framerate 30 mnevniki/stage/export/merge-audio-instagram.MP4
```

#### convert video for twitter
```
./avm/enc-twitter.sh opolchenie/stage/export/merge.MP4  opolchenie/stage/export/merge-twitter.MP4
```

./avm/gopro120to60.sh opolchenie/20210402-07.MP4  opolchenie/stage/20210402-07.MP4

