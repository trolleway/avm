# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='change video fps with generate new frames',
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
    if 'codec_name=mjpeg' in ffmpeg_result:
        return 'mjpeg'
    return 'h264'
    
parser = argparser_prepare()
args = parser.parse_args()
src = args.path
fps = args.fps

#dst=$(dirname $1)/$(basename $1| cut -d. -f1)-48fps.mp4

temp_mp4 = os.path.splitext(src)[0]+'-'+'temp'+'.mp4'
dst = os.path.splitext(src)[0]+'-'+str(fps)+'.webm'

if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)
    

source_codec = determine_codec(src)


if source_codec == 'mjpeg':
    cmd = '''
    ffmpeg -hide_banner -loglevel error -i {src} -y -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps={fps}'" -c:v libx264 -crf 0 -preset ultrafast  {temp_mp4}
    
ffmpeg -hide_banner -loglevel error -i {temp_mp4} -vf scale=-1:720 -c:v libvpx-vp9 -b:v 0 -crf 27 -row-mt 1 -pix_fmt yuv420p -c:a libopus  -movflags use_metadata_tags {dst}

'''    
    cmd_not_working = '''
    ffmpeg -hide_banner -loglevel error -i {src} -y -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps={fps}'"  -filter:v scale=-1:720 -c:v libvpx-vp9 -b:v 0 -crf 27 -row-mt 1 -pix_fmt yuv420p -c:a libopus  -movflags use_metadata_tags {dst}

'''
    cmd = cmd.format(src=src, dst=dst, fps=fps,temp_mp4=temp_mp4)
    print(cmd)
    os.system(cmd)
    if os.path.exists(temp_mp4):os.unlink(temp_mp4)

elif source_codec == 'h265':
    quit('interpolation not implement')
    cmd = '''
ffmpeg -hide_banner -loglevel error -i {src}  -y -map 0:v -c:v copy -bsf:v  hevc_mp4toannexb raw.h265
	ffmpeg -hide_banner -loglevel error -fflags +genpts -r {fps}  -y -i raw.h265 -c:v copy {dst}

'''
    cmd = cmd.format(src=src, dst=dst, fps=fps)
    os.system(cmd)
    os.unlink('raw.h265')
    
elif source_codec == 'h264':
    quit('interpolation not implement')
    cmd = '''
    ffmpeg -hide_banner -loglevel error -i {src}  -y -map 0:v -c:v copy -bsf:v  h264_mp4toannexb  raw.h264
	ffmpeg -fflags +genpts -r {fps}  -y -i raw.h264 -c:v copy {dst}
'''
    cmd = cmd.format(src=src, dst=dst, fps=fps)
    os.system(cmd)
    os.unlink('raw.h264')
    
    
    