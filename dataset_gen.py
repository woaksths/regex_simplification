#!/usr/bin/env python
# coding: utf-8


from FAdo.fa import *
from FAdo.reex import *
import pickle
import argparse


parser = argparse.ArgumentParser(description='')
parser.add_argument('--path', required=True, help='dataset path')
args = parser.parse_args()


def get_dfa_from_re(regex):
    regex= str2regexp(regex)
    return regex.toDFA()


def permutation(states_index):
    if len(permuted_states_list) == len(states_index):
        states_order.append(' '.join(map(str,permuted_states_list)))
    else:
        for idx, st_idx in enumerate(states_index):
            if visited[idx]:
                continue
            visited[idx] = True
            permuted_states_list.append(st_idx)
            permutation(states_index)
            visited[idx]= False
            permuted_states_list.remove(permuted_states_list[-1])


def generate_eq_regexes(regex):
    global permuted_states_list
    global visited 
    global states_order
    dfa = get_dfa_from_re(regex)
    permuted_states_list = list()
    states_index = dfa.indexList(dfa.States)
    
    # get permutations of state index 
    visited = [False for _ in range(len(states_index))]
    states_order = list()
    permutation(states_index)

    regex_set = dict()
    regex_set['origin'] = regex
    regex_set['complex'] = set()
    # mdfa regex 
    regex_set['complex'].add(str(dfa.dup().minimal().reCG().reduced()).replace(' ',''))
    # state elimination 
    for order in states_order:
        st_idx_order = (list(map(int, order.split(' '))))
        dfa_temp = dfa.dup()
        generated_re = str(dfa_temp.re_stateElimination(st_idx_order).reduced()).replace(' ','')
        regex_set['complex'].add(generated_re)
    return regex_set


input_file = args.path
output_file = args.path.split('.')[0] +'_dataset.pickle'


with open(input_file,'rb') as rf:
    regex_set = pickle.load(rf)
    pair_dataset = []
    for idx, regex in enumerate(regex_set):
        print('current {} th '.format(idx))
        if len(get_dfa_from_re(regex).States) <= 8:
            print('processing {} th regex {}'.format(idx,regex))
            pair_dataset.append(generate_eq_regexes(regex))

            
with open(output_file, 'wb') as f:
    pickle.dump(pair_dataset, f, pickle.HIGHEST_PROTOCOL)
