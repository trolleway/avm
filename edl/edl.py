# -*- coding: utf-8 -*-

import csv, os, shutil, argparse, errno
import glob

def argparser_prepare():

    class PrettyFormatter(argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):

        max_help_position = 35

    parser = argparse.ArgumentParser(description='',
            formatter_class=PrettyFormatter)
    parser.add_argument( 'edl', type=str, 
                        help='path to edl')

    return parser
    
parser = argparser_prepare()
args = parser.parse_args()
edl_filename = args.edl

if not(os.path.isfile(edl_filename)):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), edl_filename)

commands = list()
with open(edl_filename) as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    
    
    for line in read_tsv:
        tsv_line = list()

        if str(line)=='': continue
        if line==[]: continue
        if line[0].startswith('#'): continue
        if str(line[0]).startswith('#'): continue
        
        #print(line)
        
        for element in line:
            if element != '' and '#' not in element: tsv_line.append(element)
        print(tsv_line)
        # parse each string to tuple with standart parameters
        command = {'command':'pull_video', 'filename': tsv_line[0]}
        if len(tsv_line) > 1: command['from']= tsv_line[1]
        if len(tsv_line) > 2: command['duration']= tsv_line[2]
        commands.append(command)
        
#initialize files and dirs
basedir = os.path.dirname(os.path.realpath(edl_filename))
tempdir = os.path.join(basedir,'tmp')
if os.path.exists(tempdir): shutil.rmtree(tempdir)
if not(os.path.exists(tempdir)): os.mkdir(tempdir)

temp_clip_counter=0


for command in commands:
    if command['command']=='pull_video':
        temp_clip_counter += 1
        cnt_str = str(temp_clip_counter).zfill(6)
        
        start = ''
        if 'from' in command: start = '-ss '+command['from']
        
        duration = ''
        if 'duration' in command: duration = '-t '+command['duration']
        
        cmd  = '''ffmpeg -y  -hide_banner {start} -accurate_seek  {duration} -loglevel error -i {src} -c copy  -f mpegts {ts_file}   '''
        cmd = cmd.format(src=os.path.join(basedir,command['filename']), start=start, duration = duration, ts_file = os.path.join(tempdir,cnt_str+'.ts'))
        print(cmd)
        os.system(cmd)
        
#merge temp clips to result file
        
temp_clips = glob.glob(os.path.join(tempdir,'*.ts'))
concat = 'concat:' 
concat += '|'.join(temp_clips)
        
print(concat)

cmd = '''ffmpeg -y  -hide_banner -loglevel error -i "{concat}" -c copy -bsf:a aac_adtstoasc {path}'''
cmd = cmd.format(concat = concat,path=os.path.join(basedir,os.path.splitext(os.path.basename(edl_filename))[0]+'_montage.mp4'))
print(cmd)
os.system(cmd)

         