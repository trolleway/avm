# -*- coding: utf-8 -*-

import argparse
import subprocess
import os


def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='Stabilize video from GoPro Time Lapse',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'src', type=str, 
                        help='path to file')    

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
src = args.src


#dst=$(dirname $1)/$(basename $1| cut -d. -f1)-48fps.mp4
dst = os.path.splitext(src)[0]+'-'+'stab'+'.mp4'

if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)
    


cmd = '''
 ffmpeg -i {src} -y -vf vidstabdetect -f null transforms.trf
 ffmpeg -i {src} -y -vf vidstabtransform=smoothing=10:maxangle=0.15:input=transforms.trf  -crf 17 {dst}

'''
cmd = cmd.format(src=src, dst=dst)
os.system(cmd)
os.unlink('transforms.trf')
