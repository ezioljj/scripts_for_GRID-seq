import os
import re
from collections import defaultdict
from sys import argv

script, sample = argv

def process_fastq(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

def sequence_reverse_complementary(input_sequence):
    '''This is for RNA reads obtained by DNA-linker, we need to reverse and complement it to get the original RNA sequence'''
    reversed = input_sequence[::-1]
    tmp = []
    for i in reversed:
        if i == 'A' or i == 'a':
            tmp.append('T')
        elif i == 'T' or i == 't':
            tmp.append('A')
        elif i == 'C' or i == 'c':
            tmp.append('G')
        elif i == 'G' or i == 'g':
            tmp.append('C')
        else:
            tmp.append(i)
            
    return ''.join(tmp)

def process_target_sequence(pure_sequence, quality_sequence, tag):
    '''This function is used to get the exact 18-20 bp sequence out from rough target sequence'''
    RNA_linker = re.compile(r'GTTGGA' + r'[ATCGatcgnN]{21}' + r'CACACACCGAACTCCAAC')
    DNA_linker = re.compile(r'GTTGGAGTTCGGTGTGTG' + r'[ATCGatcgnN]{21}' + r'TCCAAC')
    #strict_linker = re.compile(r'GTTGGA' + r'[ATCGatcgnN]{21}' + r'CACACACCGAACTCCAACT')
    RNA_match = RNA_linker.findall(pure_sequence)
    DNA_match = DNA_linker.findall(pure_sequence)
    if tag == 'RNA' and len(RNA_match) == 1:
        linker_loci = pure_sequence.index(RNA_match[0])
        RNA_reads = pure_sequence[:linker_loci]
        RNA_quality = quality_sequence[:linker_loci]
        DNA_reads = pure_sequence[linker_loci + 45:linker_loci + 45 + 23]
        DNA_quality = quality_sequence[linker_loci + 45:linker_loci + 45 + 23]
        return DNA_reads, DNA_quality, RNA_reads, RNA_quality
    elif tag == 'DNA' and len(DNA_match) == 1:
        linker_loci = pure_sequence.index(DNA_match[0])
        DNA_reads = pure_sequence[:linker_loci]
        DNA_quality = quality_sequence[:linker_loci]
        RNA_reads = pure_sequence[linker_loci + 45:linker_loci + 45 + 23]
        RNA_quality = quality_sequence[linker_loci + 45:linker_loci + 45 + 23]
        return DNA_reads, DNA_quality, RNA_reads, RNA_quality
    else:
        DNA_reads = pure_sequence
        DNA_quality = quality_sequence
        RNA_reads = pure_sequence
        RNA_quality = quality_sequence
        return DNA_reads, DNA_quality, RNA_reads, RNA_quality

def count_linked(input_file, DNA_output, RNA_output):
    '''This function is used to get the target sequence out (both raw DNA and RNA) with their information'''
    n = 4
    m = 370337003
    DNA_linker = re.compile(r'GTTCGGTGTGTG')
    RNA_linker = re.compile(r'CACACACCGAAC')
    with open(input_file, 'rt') as f, open(DNA_output, 'wt') as F1, open(RNA_output, 'wt') as F2:
        lines = []
        for line in f:
            lines.append(line.rstrip())
            if len(lines) == n:
                record = process_fastq(lines)
                RNA = RNA_linker.search(record['sequence'])
                DNA = DNA_linker.search(record['sequence'])
                if RNA:
                    DNA_reads, DNA_quality, RNA_reads, RNA_quality = process_target_sequence(record['sequence'], record['quality'], 'RNA')
                    m = m + 1
                    print('@' + str(m), file = F1)
                    #we add this because we failed to add T during experiment, so the T belongs to the linker, not belong to the sequencing sample itself
                    if DNA_reads.startswith(('t', 'T')):
                        print(DNA_reads[1:], file = F1)
                        print('+', file = F1)
                        print(DNA_quality[1:], file = F1)
                    else:
                        print(DNA_reads, file = F1)
                        print('+', file = F1)
                        print(DNA_quality, file = F1)
                    print('@' + str(m), file = F2)
                    print(RNA_reads, file = F2)
                    print('+', file = F2)
                    print(RNA_quality, file = F2)              
                elif DNA:
                    DNA_reads, DNA_quality, RNA_reads, RNA_quality = process_target_sequence(record['sequence'], record['quality'], 'DNA')
                    m = m + 1
                    print('@' + str(m), file = F1)
                    print(DNA_reads, file = F1)
                    print('+', file = F1)
                    print(DNA_quality, file = F1)
                    print('@' + str(m), file = F2)
                    print(sequence_reverse_complementary(RNA_reads), file = F2)
                    print('+', file = F2)
                    print(RNA_quality[::-1], file = F2)
                lines = []

path='./trim_statistics/'

count_linked(path + sample, path + 'DNA_reads.' + sample, path + 'RNA_reads.' + sample)

            

            
            
            

            
            
            
            
            
            
            
            
            
            
            
            
            
                    
