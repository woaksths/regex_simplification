#!/usr/bin/env python
# coding: utf-8

import rstr
import re
import time 

symbols = ['0', '1', '(', ')', '*', '+']

def check_valid(regex):
    try:
        p = re.compile(regex)
        is_valid = True
    except re.error:
        is_valid = False    
    # re.compile do not catch the below exception cases 
    if '()' in regex or '+)' in regex or '(+' in regex     or regex[-1] =='+' or regex[0] =='+' or '++' in regex: 
        is_valid = False
    return is_valid


start = time.time()
valid_regexs = set()

print('regex generate start!!!')

while True:
    regex = rstr.rstr(symbols,1,30)
    if regex.strip() =='':
        continue
    if check_valid(regex):
        valid_regexs.add(regex)
    if len(valid_regexs) == 100000:
        break

print('Total time {}'.format(time.time()-start))

with open('regex_set.txt', 'w') as fw:
    for regex in valid_regexs:
        fw.write(regex +'\n')
