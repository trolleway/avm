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

def get_twitter_filepath(filepath):
    """
    Takes a file path and returns a new path with '-twitter' 
    appended before the file extension.
    """
    # Split the path into the root (everything before the extension) and the extension
    base, ext = os.path.splitext(filepath)
    
    # Rejoin them with the new suffix
    return f"{base}-twitter{ext}"
    
parser = argparser_prepare()
args = parser.parse_args()
src = args.path


if os.path.isfile(src):
    dst = get_twitter_filepath(src)
    cmd = [
    'ffmpeg', 
    '-i', src, 
    '-y', 
    '-vf', 'scale=1920:1080,format=yuv420p',  # Combined filters
    '-c:v', 'libx264', 
    '-crf', '28', 
    '-c:a', 'aac', 
    '-movflags', '+faststart', 
    '-preset', 'fast', 
    dst
]

    subprocess.run(cmd)
elif path != '':
    cmd = '''wget -O- $url | ffmpeg -i - -y  -c:v libx264  -crf 24 -preset fast -c:a libmp3lame v/twitter.mp4'''
    cmd = cmd.replace('$url',path)
    print(cmd)
    os.system(cmd)
else:
    quit('not found' + path)
