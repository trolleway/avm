# -*- coding: utf-8 -*-

import os,sys,argparse
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='Overlay map on GoPro videos',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'path', type=str, 
                        help='path to folder')    

    return parser
    

def print_command(cmd:list):
    print(' '.join(cmd))

parser = argparser_prepare()
args = parser.parse_args()
path = args.path


if not os.path.isdir(path):
    sys.exit("not found directory "+os.path.abspath(path))

cmd = ['./merge.sh',path]
print_command(cmd)
merge_result='2024-04-29.mp4'


cmd_text = r'''docker run --rm --mount="type=bind,source=c:\trolleway\avm\video,target=/video/" thomergil/gpxmapmovie    --tms-url-template 'https://trolleway.com/tiles/youtube/{zoom}/{x}/{y}.png'   --tail-duration 10000   --pre-draw-track --line-width 4  --pre-draw-track-color '#808080' --zoom 16  --viewport-height 800  --viewport-width 800 --margin 100 --information-position hidden '''

for entry in os.scandir(path):
    if entry.is_file():
        cmd_text += ' --input /'+os.path.join('video',entry.name)+' '

cmd_text += ' --output /video/overlay-detail.mp4'

cmd_text += "\n"


with open("temp_map.ps1", "w") as text_file:
    text_file.write(cmd_text)
print('printed to temp_map.ps1')


cmd_text = r'''time ffmpeg -y -i '''+path+'''/merge/'''+merge_result+''' -i '''+path+'''/overlay-detail.mp4    -filter_complex "[0:v][1:v]overlay=x=(main_w-overlay_w):y=(main_h-overlay_h)"  -map 0:a? -c:v libx264 -crf 18  -c:a copy '''+path+'''/combined.mp4'''
print(cmd_text)