import numpy as np
from scipy import stats
import re, os
from collections import defaultdict

def make_dict(input_file):
    '''we will make dict for each bin'''
    big_dict = defaultdict(list)
    RNA_dict = defaultdict(list)
    with open(input_file, 'rt') as f:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            id = line_list[3]
            big_dict[id]
            RNA_dict[id]
    return big_dict, RNA_dict

def prepare_for_zscore(dict_file, input_file, output_file, cutoff):
    '''we will calculate zscore for each bin'''
    big_dict, RNA_dict = make_dict(dict_file)
    with open(input_file, 'rt') as f, open(output_file, 'wt') as F:
        for line in f:
            line_list = re.split(r'\t', line.strip())
            id = line_list[3]
            interaction = float(line_list[-1])
            RNA = line_list[-2]
            big_dict[id].append(interaction)
            RNA_dict[id].append(RNA)
            
        for i in big_dict:
            if big_dict[i]:
                tmp = np.array(big_dict[i])
                zscore_list = list(stats.zscore(tmp))
                std = np.std(zscore_list, ddof = 1)
                bin_count = len(zscore_list)
                hscore = max(zscore_list)
                RNA_list = list(set(RNA_dict[i]))
                # count is the count for zscore larger than cutoff, bin_count is the count for valid caRNA interaction
                print(i, hscore, ','.join(RNA_list), std, bin_count, sep = '\t', file = F)
            else:
                print(i, np.nan, np.nan, np.nan, np.nan, sep = '\t', file = F)
                
prepare_for_zscore('A_compartment.0h.500kb', '02.merged.0h.A_interaction', '03.merged.0h.hscore', 2.5)
prepare_for_zscore('A_compartment.60h.500kb', '02.merged.60h.A_interaction', '03.merged.60h.hscore', 2)