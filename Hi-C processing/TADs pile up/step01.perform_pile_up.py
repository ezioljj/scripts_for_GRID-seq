import coolbox
from coolbox.api import *
import matplotlib.pyplot as plt
import re
import pandas as pd
import numpy as np
from sys import argv

script, time, input_file, output_file = argv

normalize_method = 'expect'

hic_0h = '/home/ljj/C2C12/00.files/cool/0h.allvalidPairs.hic'
hic_60h = '/home/ljj/C2C12/00.files/cool/60h.allvalidPairs.hic'

dhic_0h = DotHiC(hic_0h, normalize = normalize_method)
dhic_60h = DotHiC(hic_60h, normalize = normalize_method)

def pile_up_for_matrix(target_region, time, res = 10000, flanking_bin = 20, mini_bin = 40):
    '''according to the input region, we will get a large area for normalization, then we get the target region out.'''
    # target region preparation
    target_list = re.split(r'[:-]', target_region)
    chr = target_list[0]
    start = int(target_list[1])
    end = int(target_list[2])
    
    # the size of our target region (small region)
    target_bin = abs(start - end) // res
    if target_bin >= mini_bin:
        # the whole large matrix
        large_start = start - flanking_bin * res
        large_end = end + flanking_bin * res
        large_target = chr + ':' + str(large_start) + '-' + str(large_end)
        
        # the region for pile up
        #small_start = end - flanking_bin * res
        #small_end = end + flanking_bin * res
        #small_target = chr + ':' + str(small_start) + '-' + str(small_end)
        
        # here i need to know the sort of y-axis and x-axis 
        try:
            if time == '0h':
                matrix = dhic_0h.fetch_data(large_target, resolution = res)
                loci = matrix.shape[1]
                mat = matrix[:2 * flanking_bin, loci - 2 * flanking_bin:]
                return mat
            elif time == '60h':
                matrix = dhic_60h.fetch_data(large_target, resolution = res)
                loci = matrix.shape[1]
                mat = matrix[:2 * flanking_bin, loci - 2 * flanking_bin:]
                return mat
        # this is because we may have region exceed the actual chromosome size
        except:
            matrix = np.full((flanking_bin, flanking_bin), np.nan)
            return matrix
    else:
        matrix = np.full((flanking_bin, flanking_bin), np.nan)
        return matrix

def get_interaction(time, input_file, output_file):
    '''we will get interaction'''
    big_list = []
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            region = line_list[0]
            matrix = pile_up_for_matrix(region, time)
#             print(a)
#             print(matrix)
#             print(matrix.shape)
            if np.isnan(matrix).any():
                pass
            else:
                big_list.append(matrix)
    
#     for i in big_list:
#         print(i)
#         print(i.shape)
    
    final_mat = sum(big_list) / len(big_list)
    
    np.savetxt(output_file, final_mat, delimiter='\t', fmt = '%.4f')
            
get_interaction(time, input_file, output_file)            
