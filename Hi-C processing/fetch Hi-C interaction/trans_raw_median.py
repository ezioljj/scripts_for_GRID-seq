import coolbox
from coolbox.api import *
import matplotlib.pyplot as plt
import re
import pandas as pd
import numpy as np
from sys import argv

script, input_region = argv

hic_0h = '/home/ljj/C2C12/00.files/cool/0h.allvalidPairs.hic'
hic_60h = '/home/ljj/C2C12/00.files/cool/60h.allvalidPairs.hic'

dhic_0h = DotHiC(hic_0h, resolution = 100000)
dhic_60h = DotHiC(hic_60h, resolution = 100000)

def calculate_change_of_hic(region_1, region_2, time, resolution=100000):
    '''according to the input region, we will calculate the total sum of target region at 0h and 60h, 
    then we can calculate the change
    1) if region_1 == region_2, then we get cis interaction matrix;
    2) if region_1 != region_2, then we get trans interaction matrix.'''
    try:
        if time == '0h':
            matrix = dhic_0h.fetch_data(region_1, region_2, resolution)
        elif time == '60h':
            matrix = dhic_60h.fetch_data(region_1, region_2, resolution) / 1.086
        return np.median(matrix)
    except:
        return np.nan

def get_interaction(input_file, output_file):
    '''we will get interaction'''
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            region_1 = line_list[0]
            region_2 = line_list[1]
            RNA_1 = line_list[2]
            RNA_2 = line_list[3]
            interaction_0h = calculate_change_of_hic(region_1, region_2, '0h')
            interaction_60h = calculate_change_of_hic(region_1, region_2, '60h')
            print(region_1, region_2, RNA_1, RNA_2, interaction_0h, interaction_60h, sep = '\t', file = F)
            
get_interaction(input_region, input_region + '.raw')