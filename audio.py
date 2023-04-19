#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():
    parser = argparse.ArgumentParser(description='add audio to video')
    parser.add_argument( 'video', type=str, 
                        help='path to file')    
    parser.add_argument( 'audio', type=str, 
                        help='audio file')
    parser.add_argument('-m','--mix', action="store_const", required=False, default=False, const=True, help='mix audio with exist in video')
    return parser
    

parser = argparser_prepare()
args = parser.parse_args()
src = args.video
audio = args.audio
dst = os.path.splitext(src)[0]+'-'+'audio'+'.mp4'

if not(os.path.isfile(src)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src)

if not(os.path.isfile(audio)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), audio)

if  args.mix == False:    
  cmd = 'ffmpeg -i {src} -i {audio} -y -c:v copy -map 0:v -map 1:a -c:v copy -shortest {dst}'
elif args.mix == True:
  cmd = 'ffmpeg -i {src} -i {audio} -y -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -ac 2 -shortest  {dst}'
cmd = cmd.format(src=src, audio=audio, dst = dst)
os.system(cmd)
        
