import re, os
from collections import defaultdict
from itertools import combinations

def make_dict_for_top_bottom(RNA, time):
    '''we will prepare for top bottom 10% combinations'''
    # top
    big_dict = dict()
    with open('top10.' + RNA + '.' + time + '.500kb', 'rt') as f:
        for line in f:
            if not line.startswith('id'):
                line_list = re.split(r'\t', line.strip())
                id = line_list[0]
                fc = line_list[1]
                big_dict[id] = big_dict.get(id, fc)
                
    with open('top10.' + RNA + '.' + time + '.500kb.combinations', 'wt') as F:
        combination_list = list(combinations(big_dict.keys(), 2))
        for i in combination_list:
            print(i[0], i[1], big_dict[i[0]], big_dict[i[1]], sep = '\t', file = F)
    
    # bottom        
    big_dict = dict()
    with open('bot10.' + RNA + '.' + time + '.500kb', 'rt') as f:
        for line in f:
            if not line.startswith('id'):
                line_list = re.split(r'\t', line.strip())
                id = line_list[0]
                fc = line_list[1]
                big_dict[id] = big_dict.get(id, fc)
                
    with open('bot10.' + RNA + '.' + time + '.500kb.combinations', 'wt') as F:
        combination_list = list(combinations(big_dict.keys(), 2))
        for i in combination_list:
            print(i[0], i[1], big_dict[i[0]], big_dict[i[1]], sep = '\t', file = F)
            
for i in ['Fn1', 'Neat1', 'Macf1', 'Runx1']:
    make_dict_for_top_bottom(i, '60h')
    
make_dict_for_top_bottom('Hmga2', '0h')
            