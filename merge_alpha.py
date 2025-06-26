# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='merge video in folder without recompress',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'path', type=str, 
                        help='path to folder')    


    return parser
    

def determine_codec(filename):
    command = ['ffprobe', '-show_format', '-pretty', '-show_entries', 'stream=codec_name', '-loglevel', 'quiet', filename]
    print(' '.join(command))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
    ffmpeg_result = out.decode()

    if 'codec_name=hevc' in ffmpeg_result:
        return 'h265'
    if 'codec_name=mjpeg' in ffmpeg_result:
        return 'mjpeg'
    return 'h264'
    
def get_dir_filenames(path,ext)->list:

    files=list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(ext.lower()):
                files.append(os.path.join(root, file))
    return files

def list2textfile(items:list,filepath:str):
    with open(filepath, "w") as file:
        for item in items:
            file.write('file '+item)
                 
parser = argparser_prepare()
args = parser.parse_args()
folder = args.path

if not(os.path.isdir(folder)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), folder)
files = get_dir_filenames(folder,'.avi')
assert len(files)>0

print(files)
source_codec = determine_codec(os.path.join(folder,files[0]))
listfile='list.txt'
list2textfile(files,listfile)

dstfilebase = os.path.splitext(files[0])[0]+'-merge'




if source_codec == 'mjpeg':
    dst=dstfilebase+'.avi'
    cmd = ['ffmpeg','-f','concat','safe',0,'-i',listfile,'-c','copy',dst]
    print(' '.join(cmd))
    subprocess.run(cmd)
    quit()
    os.unlink(listfile)
    print('finished')
    print(dst)
    
    
else:
    print('h264 detected')
    
    #merge mp4 files (h264 or 265) withouth encoding

    SRC=$1 #folder
    DST=$SRC/merge
    DATE=$(date +%Y-%m-%d)

    #create dir if not exists
    mkdir -p  $DST
    #convert to mpeg transport stream
    for f in $1/*.[mM][pPKk][4vV]; do ffmpeg -y  -hide_banner -loglevel error -i $f -c copy  -f mpegts $DST/$(basename $f| cut -d. -f1).ts; done
    LIST='concat:'
    for f in $DST/*.ts; do LIST+="$f|" ; done
    #merge
    ffmpeg -y  -hide_banner -loglevel error -i "$LIST" -c copy -bsf:a aac_adtstoasc $DST/$DATE.mp4

    rm -rf $DST/*.ts
    rm -rf $DST/list.txt



    '''
    #create dir if not exists
    mkdir -p  $DST
    #convert to mpeg transport stream
    for f in $1/*.[mM][pPKk][4vV]; do ffmpeg -y  -hide_banner -loglevel error -i $f -c copy  -f mpegts $DST/$(basename $f| cut -d. -f1).ts; done
    LIST='concat:'
    for f in $DST/*.ts; do LIST+="$f|" ; done
    #merge
    ffmpeg -y  -hide_banner -loglevel error -i "$LIST" -c copy -bsf:a aac_adtstoasc $DST/$DATE.mp4

    rm -rf $DST/*.ts
    rm -rf $DST/list.txt
    
    '''


    
    