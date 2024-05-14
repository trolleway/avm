# avm
avm: Android Video Montage. Montage in a bash. Toolset for non-recompressing 4K video editing in Android Termux or Docker.

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


#### add audio to video
```
python3 audio.py video.mp4 audio.m4a
```
Produce two videofiles: with changed audio track, and with mixed audio track

#### convert video for twitter
```
./avm/enc-twitter.sh opolchenie/stage/export/merge.MP4  opolchenie/stage/export/merge-twitter.MP4
```

./avm/gopro120to60.sh opolchenie/20210402-07.MP4  opolchenie/stage/20210402-07.MP4


## Overlay map on GoPro video

### Stabilize GoPro timelapse
```
time ffmpeg -i 1.MP4 -vf vidstabdetect -f null 1.temp
time ffmpeg -i 1.MP4 -vf vidstabtransform=smoothing=5:input=transforms.trf 1.stab.MP4
```

## Merge GoPro timelapse
```
python3 ../../stab.py  1.MP4 && python3 ../../stab.py 2.MP4 && python3 ../../stab.py 3.MP4 &&  python3 ../../stab.py 4.MP4
mkdir stabs
mv *-stab.mp4 stabs/
../../merge.sh stabs
mv stabs/merge/2023-05-30.mp4 stab-merge.mp4
```

For 4K video a special map rendering with high ppi needed. These tools can not use MapBox retina tiles. So i created a special map style in MapBox with big labels. 
Insert yor own api key in URLs

### generate map overlay for list of gopro videos

```
docker run --rm -v "${PWD}:/opt/avm"  -it avm:latest python3 gopro_map.py videos  
```


```
docker run --rm --mount="type=bind,source=c:\trolleway\avm\video\merge\,target=/videos/" thomergil/gpxmapmovie    --tms-url-template 'https://trolleway.com/tiles/youtube/{zoom}/{x}/{y}.png?apikey='   --tail-duration 0   --pre-draw-track --line-width 4  --pre-draw-track-color '#808080' --zoom 15 --viewport-width 500 --viewport-height 500  --width 800 --height 800 --margin 700  --viewport-inertia 105 --information-position hidden  --input /videos/1.MP4  --input /videos/2.MP4  --input /videos/3.MP4  --input /videos/4.MP4   --output /videos/overlay-detail.mp4
```

### generate map overlay for list of gopro videos v2

```
docker run --rm --mount="type=bind,source=c:\trolleway\avm\video\merge\,target=/videos/" thomergil/gpxmapmovie    --tms-url-template 'https://trolleway.com/tiles/youtube/{zoom}/{x}/{y}.png'   --tail-duration 10000   --pre-draw-track --line-width 4  --pre-draw-track-color '#808080' --zoom 16  --viewport-height 800  --viewport-width 800 --margin 100 --information-position hidden   --input /videos/1.MP4  --input /videos/2.MP4  --input /videos/3.MP4  --input /videos/4.MP4   --output /videos/overlay-detail.mp4

```
https://trolleway.com/tiles/youtube/{zoom}/{x}/{y}.png?apikey=

### low-zoom map overlay. map zoom level hard-coded
```
docker run --rm --mount="type=bind,source=c:\trolleway\avm\video\merge\,target=/videos/" thomergil/gpxmapmovie    --tms-url-template 'https://api.mapbox.com/styles/v1/trolleway/cli8zdgj102q701qu2w8b3d4s/tiles/256/{zoom}/{x}/{y}?access_token='   --tail-duration 10000   --pre-draw-track --line-width 8  --pre-draw-track-color '#808080' --height 1000 --width 1000 --zoom 9  --information-position hidden --marker-size 12  --input /videos/1.MP4  --input /videos/2.MP4  --input /videos/3.MP4  --input /videos/4.MP4   --output /videos/overlay-big.mp4

```

### overlay map on video
overlay-big appear for 3 seconds at begin of video

```
time ffmpeg -y -i stab-merge.mp4 -i overlay-detail.mp4 -i overlay-big.mp4   -filter_complex "[0:v][1:v]overlay=main_w-overlay_w:0[step1];[step1][2:v]overlay=0:0:enable='between(t,0,3)'[step2]" -map "[step2]" -map 0:a? -c:v libx264 -crf 18  -c:a copy combined.mp4


```

 
 