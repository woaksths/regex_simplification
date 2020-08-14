#!/usr/bin/env python
# coding: utf-8

import rstr
import re
import time 
from FAdo.fa import *
from FAdo.reex import *
import pickle

def check_valid(regex):
    try:
        p = re.compile(regex)
        is_valid = True
    except re.error:
        is_valid = False    
    # re.compile do not catch the below exception cases 
    if '()' in regex or '+)' in regex or '(+' in regex or regex[-1] =='+' or regex[0] =='+' or '++' in regex: 
        is_valid = False
    return is_valid


def complex_re_gen(max_size):
    complex_datset = set()
    while True:
        depth = random.randrange(2,6)
        opening_nested = ''.join(['(' + rstr.rstr('01+*',0,5) for _ in range(depth)]) 
        closing_nested = ''.join([rstr.rstr('01+*',0,5)+ ')' for _ in range(depth)])  
        regex= rstr.rstr('01+',0,5) + opening_nested + closing_nested + rstr.rstr('01+',0,5)
        if check_valid(regex):
            if len(str2regexp(regex).toDFA().States) <= 10:
                complex_datset.add(regex)
        if len(complex_datset) == max_size:
            break
    return complex_datset


symbols = ['0', '1', '(', ')', '*', '+']
start = time.time()
simple_regexs = set()

print('regex generate start!!!')
while True:
    regex = rstr.rstr(symbols,1,30)
    if regex.strip() =='' or not check_valid(regex):
        continue
    if len(str2regexp(regex).toDFA().States) <= 10:
        simple_regexs.add(regex)
    if len(simple_regexs) == 70000:
        break
        
complex_regexs = complex_re_gen(30000)
print('Total time {}'.format(time.time()-start))
total_regexs = simple_regexs | complex_regexs

with open('simple_regexs.pickle', 'wb') as f:
    pickle.dump(simple_regexs, f, pickle.HIGHEST_PROTOCOL)

with open('complex_regexs.pickle', 'wb') as f:
    pickle.dump(complex_regexs, f, pickle.HIGHEST_PROTOCOL)

with open('total_regexs.pickle', 'wb') as f:
    pickle.dump(total_regexs, f, pickle.HIGHEST_PROTOCOL)

