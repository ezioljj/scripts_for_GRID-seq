import os
import re
from collections import defaultdict
from sys import argv

script, sample = argv

def process_fastq(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

def count_linked(input_file, linker_succeed, no_linker):
    '''This function is used to get the target sequence out (both raw DNA and RNA) with their information'''
    n = 4
    m = 0
    DNA_linker = re.compile(r'GTTCGGTGTGTG')
    RNA_linker = re.compile(r'CACACACCGAAC')
    with open(input_file, 'rt') as f, open(linker_succeed, 'wt') as F1, open(no_linker, 'wt') as F6:
        lines = []
        for line in f:
            lines.append(line.rstrip())
            if len(lines) == n:
                record = process_fastq(lines)
                RNA = RNA_linker.search(record['sequence'])
                DNA = DNA_linker.search(record['sequence'])
                if RNA or DNA:
                    print(record['name'], file = F1)
                    print(record['sequence'], file = F1)
                    print('+', file = F1)
                    print(record['quality'], file = F1)
                else:
                    print(record['name'], file = F6)
                    print(record['sequence'], file = F6)
                    print('+', file = F6)
                    print(record['quality'], file = F6)               
                lines = []

count_linked(sample, 'linker.' + sample, 'nolinker.' + sample)


            
            
            
            
            
            
            
            
            
            
            
                    
            