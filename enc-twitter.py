# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='encode video for twitter',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'path', type=str, 
                        help='path to file or http url')    

    return parser
    



def is_url_exists(url):
    return requests.head(url).status_code < 400
    
parser = argparser_prepare()
args = parser.parse_args()
path = args.path

print(path)
if os.path.isfile(path):
    cmd='''
    SRC=$1
DST=$(dirname $1)/$(basename $1| cut -d. -f1)-twitter.mp4
ffmpeg -i $SRC -y -vf scale=1920:1080 -c:v libx264  -crf 24 -preset fast -c:a copy $DST
'''
    cmd = cmd.replace('$1',path)
    os.system(cmd)
elif path != '':
    cmd = '''wget -O- $url | ffmpeg -i - -y  -c:v libx264  -crf 24 -preset fast -c:a libmp3lame v/twitter.mp4'''
    cmd = cmd.replace('$url',path)
    print(cmd)
    os.system(cmd)
else:
    quit('not found' + path)