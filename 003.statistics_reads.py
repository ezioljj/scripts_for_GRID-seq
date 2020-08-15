import os
import re
from collections import defaultdict
from sys import argv

script, sample = argv

def process_fastq(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

def process(input_file, output_file):
    n = 4
    final = dict()
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        lines = []
        for line in f:
            lines.append(line.rstrip())
            if len(lines) == n:
                d = process_fastq(lines)
                key = len(d['sequence'])
                final[key] = final.get(key, 0) + 1
                lines = []
        
        for i in sorted(final.keys()):
            if int(i) == 0 or 17 <= int(i) <= 23: 
                print(i, final[i], '%.2f' % (100 * int(final[i]) / sum(final.values())), sep = '\t', file = F)
                
path='./trim_statistics/'
            
process(path + sample, 'STA.' + sample)
                
    
