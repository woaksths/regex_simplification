#!/usr/bin/env python
# coding: utf-8

import rstr
import re
import time 
from FAdo.fa import *
from FAdo.reex import *
import pickle
from infix_to_postfix import Conversion, preprocessing_concat


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


def complex_re_gen(max_size, height=None):
    complex_dataset = set()
    while True:
        if len(complex_dataset) >0 and len(complex_dataset) % 1000 == 0:
            print('complex: current processing {}th data'.format(len(complex_dataset)))
        depth = random.randrange(1,6)
        opening_nested = ''.join(['(' + rstr.rstr('01+*',0,5) for _ in range(depth)]) 
        closing_nested = ''.join([rstr.rstr('01+*',0,5)+ ')' for _ in range(depth)])  
        regex= rstr.rstr('01+',0,15) + opening_nested + closing_nested + rstr.rstr('01+',0,15)
        if check_valid(regex):
            
            regex = preprocessing_concat(regex)
            re_obj = Conversion(len(regex))
            re_obj.infixToPostfix(regex)
            regex = re_obj.reduce(re_obj.output)
            star_height = str2regexp(regex).measure()[3]

            if star_height == height and len(str2regexp(regex).toDFA().States) < 10 and len(regex) < 35:
                complex_dataset.add(regex)
        if len(complex_dataset) == max_size:
            break
    return complex_dataset


def simple_re_gen(max_size):
    simple_regexs = set()
    symbols = ['0', '1', '(', ')', '*', '+']
    while True:
        if len(simple_regexs) > 0 and len(simple_regexs) % 1000 == 0:
            print('simple:current processing {}th data'.format(len(simple_regexs)))

        regex = rstr.rstr(symbols,1,50)
        if regex.strip() =='' or not check_valid(regex):
            continue

        regex= preprocessing_concat(regex)
        re_obj = Conversion(len(regex))
        re_obj.infixToPostfix(regex)
        regex = re_obj.reduce(re_obj.output)
        star_height = str2regexp(regex).measure()[3]

        if star_height < 1 and len(str2regexp(regex).toDFA().States) < 10 and len(regex) <35:    
            simple_regexs.add(regex)
        if len(simple_regexs) == max_size:
            break
    return simple_regexs


# star_height0_regexs = simple_re_gen(50000)
# star_height1_regexs = complex_re_gen(50000, 1)
# star_height2_regexs = complex_re_gen(50000, 2)

star_height3_regexs = complex_re_gen(50000, 3)

with open('star_height3_regexs.pickle', 'wb') as f:
    pickle.dump(star_height3_regexs, f, pickle.HIGHEST_PROTOCOL)
    
    
# with open('star_height0_regexs.pickle', 'wb') as f:
#     pickle.dump(star_height0_regexs, f, pickle.HIGHEST_PROTOCOL)

# with open('star_height1_regexs.pickle', 'wb') as f:
#     pickle.dump(star_height1_regexs, f, pickle.HIGHEST_PROTOCOL)

# with open('star_height2_regexs.pickle', 'wb') as f:
#     pickle.dump(star_height2_regexs, f, pickle.HIGHEST_PROTOCOL)