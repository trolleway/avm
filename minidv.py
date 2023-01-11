# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='convert MiniDV file to Youtube, deinterlace with increase framerate',
            formatter_class=PrettyFormatter)
    parser.add_argument('-ss','--start', type=str,required=False, help='timecode start')    
    parser.add_argument('-to','--stop', type=str,required=False, help='timecode stop')    
    parser.add_argument('src', type=str, help='path to src file')    
    parser.add_argument('dst', type=str, help='path to converted file')    


    return parser
    

parser = argparser_prepare()
args = parser.parse_args()
src = args.src
dst = args.dst
timecode_start=args.start
timecode_stop=args.stop


if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)

cmd = ['ffmpeg','-y', '-hide_banner']
if timecode_start is not None:
    cmd = cmd + ['-ss',timecode_start]
cmd.append('-accurate_seek')

if timecode_stop is not None:
    cmd = cmd + ['-to',timecode_stop]

cmd = cmd + ['-i',src,
'-filter:v',"idet,w3fdif,scale=960:720:flags=spline",
'-c:v', 'libx264',
'-crf', '18',
'-preset', 'slow', 
'-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-movflags' ,'+faststart',
dst]

'''
ffmpeg -y -hide_banner -ss 26:07 -accurate_seek  -to 45:45 -i edl/dvgrab-2012.04.21_17-57-06.avi -filter:v "idet,w3fdif,scale=960:720:flags=spline"   -c:v libx264  -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart  noginsk-cabview-720p50-2012.mp4
'''

subprocess.run(cmd)