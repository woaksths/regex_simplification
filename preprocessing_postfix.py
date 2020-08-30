#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from FAdo.fa import *
from FAdo.reex import *
import pickle
import argparse
from infix_to_postfix import Conversion, preprocessing_concat



parser = argparse.ArgumentParser(description ='Type file name')
parser.add_argument('--input_file', help='type input file path')

args = parser.parse_args()
input_fname = args.input_file

with open(input_fname,'r') as rf:
    dataset = rf.read().split('\n')
    with open('modified_{}'.format(input_fname),'w') as fw:

        for idx,d in enumerate(dataset):
            complex_re = d.split('\t')[0].replace(' ','')
            simple_re = d.split('\t')[1].replace(' ','')
            
            complex_re= preprocessing_concat(complex_re)
            simple_re = preprocessing_concat(simple_re)
            
            complex_obj = Conversion(len(complex_re))
            simple_obj = Conversion(len(simple_re))
            complex_obj.infixToPostfix(complex_re)
            simple_obj.infixToPostfix(simple_re)

            modified_c_re = complex_obj.reduce(complex_obj.output)
            modified_s_re = simple_obj.reduce(simple_obj.output)
            modified_c_re = ' '.join([char for char in modified_c_re])
            modified_s_re = ' '.join([char for char in modified_s_re])

            if idx % 1000 ==0:
                print('current {}th processing'.format(idx))
                
            if str2regexp(modified_c_re).toDFA() != str2regexp(modified_s_re).toDFA():
                print("{} th data dfa not equal".format(idx))
                break
            
            if modified_c_re == modified_s_re or len(modified_c_re) < len(modified_s_re):
                continue
            fw.write(modified_c_re + '\t' + modified_s_re +'\n')

