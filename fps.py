# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='change video speed by change fps withouth recompress',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'path', type=str, 
                        help='path to file')    
    parser.add_argument( 'fps', type=int, 
                        help='new fps')

    return parser
    

def determine_codec(filename):
    command = ['ffprobe', '-show_format', '-pretty', '-show_entries', 'stream=codec_name', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    ffmpeg_result = out.decode()
    if 'codec_name=hevc' in ffmpeg_result:
        return 'h265'
    return 'h264'
    
parser = argparser_prepare()
args = parser.parse_args()
src = args.path
fps = args.fps

#dst=$(dirname $1)/$(basename $1| cut -d. -f1)-48fps.mp4
dst = os.path.splitext(src)[0]+'-'+str(fps)+'.mp4'

if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)
    

source_codec = determine_codec(src)


if source_codec == 'h265':
    cmd = '''
ffmpeg -hide_banner -loglevel error -i {src}  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r {fps}  -y -i raw.h265 -c:v copy {dst}

'''
    cmd = cmd.format(src=src, dst=dst, fps=fps)
    os.system(cmd)
    os.unlink('raw.h265')
    
elif source_codec == 'h264':
    cmd = '''
    ffmpeg -hide_banner -loglevel error -i {src}  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r {fps}  -y -i raw.h264 -c:v copy {dst}
'''
    cmd = cmd.format(src=src, dst=dst, fps=fps)
    os.system(cmd)
    os.unlink('raw.h264')