# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno,subprocess
import glob
import datetime
import re

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
            
def convert_to_ts(h264filepaths, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    

    for file in h264filepaths:
        base = os.path.splitext(os.path.basename(file))[0]
        ts_path = os.path.join(dst_dir, f"{base}.ts")
        subprocess.run([
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-i', file, '-c', 'copy', '-f', 'mpegts', ts_path
        ])

def generate_concat_list(dst_dir):
    ts_files = glob.glob(os.path.join(dst_dir, '*.ts'))
    return 'concat:' + '|'.join(sorted(ts_files))

def merge_ts_files(concat_list, output_file):
    subprocess.run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', concat_list, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', output_file
    ])

def get_h264_filepaths(directory):
    pattern = re.compile(r'\.(mp4|mkv)$', re.IGNORECASE)
    filepaths = []

    # List all items in the directory
    for filename in os.listdir(directory):
        # Build the full path
        full_path = os.path.join(directory, filename)

        # Check if it's a file and matches the .mp4 pattern (case-insensitive)
        if os.path.isfile(full_path) and pattern.search(filename):
            filepaths.append(full_path)

    return filepaths
def cleanup_ts_files(dst_dir):
    for f in glob.glob(os.path.join(dst_dir, '*.ts')):
        os.remove(f)
                 
parser = argparser_prepare()
args = parser.parse_args()
folder = args.path

if not(os.path.isdir(folder)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), folder)
files = get_h264_filepaths(folder)
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

    os.unlink(listfile)
    print('finished')
    print(dst)
    
    
else:
    print('h264 detected')
    
    #merge mp4 files (h264 or 265) withouth encoding

    dst_dir = os.path.join(folder, 'merge')
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    output_file = os.path.join(dst_dir, f"{date_str}.mp4")

    h264filepaths = get_h264_filepaths(folder)
    
    convert_to_ts(h264filepaths, dst_dir)
    concat_list = generate_concat_list(dst_dir)
    merge_ts_files(concat_list, output_file)
    cleanup_ts_files(dst_dir)


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


    
    