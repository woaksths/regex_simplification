#!/usr/bin/env python
# coding: utf-8


from FAdo.fa import *
from FAdo.reex import *
import pickle


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
    regex_set['complex'].add(str(dfa.dup().minimal().reCG().reduced()))
    # state elimination 
    for order in states_order:
        st_idx_order = (list(map(int, order.split(' '))))
        dfa_temp = dfa.dup()
        generated_re = str(dfa_temp.re_stateElimination(st_idx_order).reduced())
        regex_set['complex'].add(generated_re)
    return regex_set


with open('regex_set.txt','r') as rf:
    regex_set = rf.read().split('\n')
    pair_dataset = []
    for regex in regex_set:
        if len(get_dfa_from_re(regex).States) <= 8:
            pair_dataset.append(generate_eq_regexes(regex))


with open('pair_dataset.pickle', 'wb') as f:
    pickle.dump(pair_dataset, f, pickle.HIGHEST_PROTOCOL)
