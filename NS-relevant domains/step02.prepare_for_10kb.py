import re, os
from collections import defaultdict
from sys import argv

script, input_file, output_file = argv

def prepare_for_certain_res(input_file, output_file):
    '''we will prepare for certain resolution'''
    big_dict = defaultdict(lambda:defaultdict(list))
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            loci = line_list[3]
            gene = line_list[-3]
            value = float(line_list[-2])
            big_dict[gene][loci].append(value)
            
        for i in big_dict:
            for j in big_dict[i]:
                loci_list = re.split(r'[:-]', j)
                chr = loci_list[0]
                start = loci_list[1]
                end = loci_list[2]
                print(chr, start, end, i, sum(big_dict[i][j]), sep = '\t', file = F)
                
prepare_for_certain_res(input_file, output_file)