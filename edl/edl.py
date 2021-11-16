# -*- coding: utf-8 -*-

import csv

commands = list()
with open('edl.tsv') as tsvfile:
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    
    tsv_line = list()
    for line in read_tsv:
        if str(line).beginswith('#'): continue
        for element in line:
            if element != '': tsv_line.append(element)
        
        command = {'file': tsv_line[0]}
        if len(tsv_line)>1:command['from': tsv_line[1]
        if len(tsv_line)>2:command['to': tsv_line[2]
        commands.append(command)
        
for command in commands:
    print(command)