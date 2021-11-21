# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='',
            formatter_class=PrettyFormatter)
    parser.add_argument('path', type=str, 
                        help='path to images folder')

    return parser
    
parser = argparser_prepare()
args = parser.parse_args()
basedir = args.path

if not(os.path.isdir(basedir)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), basedir)
images = glob.glob(os.path.join(basedir,'*.png'))

if len(images)>0:
    for image in images:
        print(image)
        dst = os.path.join(basedir,os.path.splitext(os.path.basename(image))[0]+'.mp4')
        cmd = '''    ffmpeg -y -loop 1 -i {src} -c:v libx264 \
-t 5 -pix_fmt yuv420p \
-vf scale=w=1280:h=720:force_original_aspect_ratio=disable \
-vf "fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5" \
-r 50 {dst}'''
        cmd = cmd.format(src=image,dst=dst)
        print(cmd)
        os.system(cmd)