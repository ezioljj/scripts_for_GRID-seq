import re, os
from collections import defaultdict
import numpy as np

RNA_dict = {'Actb':'chr5', 'Fn1':'chr1', 'Lmna':'chr3', 'Malat1':'chr19', 'Rn7sk':'chr9'}

def make_dict_for_selected_bin(input_file, output_file):
    '''we will make dict for bins that have been selected from step 1'''
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            chr = line_list[0]
            id = line_list[3]
            if id in RNA_dict and chr != RNA_dict[id]:
                print(line.strip(), file = F)

for i in ['0h', '60h']:
    for j in ['rep1', 'rep2']:
        make_dict_for_selected_bin('bed6.' + j + '.' + i + '.pkbin', 'speckle_marker.' + j + '.' + i + '.pkbin')

