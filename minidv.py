# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='convert MiniDV file to Youtube, deinterlace with increase framerate',
            formatter_class=PrettyFormatter)
    parser.add_argument('--start', type=str,required=False, help='timecode start')    
    parser.add_argument('--stop', type=str,required=False, help='timecode stop')    
    parser.add_argument('--keep-interlace', action='store_true',required=False, help='skip w3fdif deinterlace process for demonstration, generate 25i instead of 50p video')    
    parser.add_argument('--preset', type=str, required=False, choices=['youtube', 'wikicommons'], default='youtube', help='preset for web service') 
    parser.add_argument('-an','--audio-no', action='store_true',required=False, help='drop audio') 
    parser.add_argument('src', type=str, help='path to src file')    
    parser.add_argument('dst', type=str, help='path to converted file')    


    return parser
    

parser = argparser_prepare()
args = parser.parse_args()
src = args.src
dst = args.dst
timecode_start=args.start
timecode_stop=args.stop
preset=args.preset
audio_no=args.audio_no

if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)

cmd = ['ffmpeg','-y', '-hide_banner']
if timecode_start is not None:
    cmd = cmd + ['-ss',timecode_start]
cmd.append('-accurate_seek')

if timecode_stop is not None:
    cmd = cmd + ['-to',timecode_stop]
cmd = cmd + ['-i',src]

if args.keep_interlace:
    cmd = cmd + ['-filter:v',"scale=960:720:flags=spline"]
else:
    cmd = cmd + ['-filter:v',"idet,w3fdif,scale=960:720:flags=spline"]
if no_audio: cmd = cmd + ['-an']
    
if preset=='youtube':
    cmd = cmd + [
'-c:v', 'libx264',
'-crf', '18',
'-preset', 'slow', 
'-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-movflags' ,'+faststart',
dst]
elif preset == 'wikicommons':


    cmd = cmd + [
'-c:v', 'libvpx-vp9',
'-quality','good',
'-crf', '27', '-b:v', '0',
'-row-mt','1',
'-pix_fmt', 'yuv420p', 
'-c:a', 'libopus', 
dst] 

print(' '.join(cmd))  

'''
time python3 minidv.py --start 00:06:31 --stop 00:06:44 --preset wikicommons dv/dvgrab-2014.09.28_12-05-43.avi dv/t2_2014-09-28_16-15-00_sadovoe_crf27_quality-good.webm 
ffmpeg -y -hide_banner -ss 26:07 -accurate_seek  -to 45:45 -i edl/dvgrab-2012.04.21_17-57-06.avi -filter:v "idet,w3fdif,scale=960:720:flags=spline"   -c:v libx264  -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart  noginsk-cabview-720p50-2012.mp4


ffmpeg -i dv/dvgrab-2014.09.28_12-05-43.avi -c:v libvpx-vp9 -lossless 1 dv/output.webm


 




'''

subprocess.run(cmd)
