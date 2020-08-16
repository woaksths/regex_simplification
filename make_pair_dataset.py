#!/usr/bin/env python
# coding: utf-8

# #### description of generating dataset
# - ground truth (simple) 정규식을 7만개는 간단한것 3만개는 다소 복잡한(nested, star etc) 정규식으로 구성 
# - state의 개수가 8개 이하인 것만을 선택하다보니 70000 -> 65004, 30000 ->20513으로 줄어듬
# - train, valid, test를 state elimination을 하여 나온 정규식에서 75%, 15%, 15% 비율로 나눔
# - epsilon transition은 고려를 하지 않되, epsilon을 뺸 데이터셋이 0개가 될 때는 skip
# ------------------------------
# #### output of dataset
# - complex_simple_train.pickle
# - complex_simple_valid.pickle
# - complex_simple_test.pickle 



import random 
import pickle

def generating_train_valid_test(pair_dataset):
    train_set = []
    valid_set = []
    test_set = []
    regex_set = set()
    
    for idx, data in enumerate(pair_dataset):
        simple_re = data['origin']
        complex_re_set = data['complex']
        
        if simple_re in regex_set:
            continue
        
        regex_set.add(simple_re)
        complex_re_set = [re for re in complex_re_set if not 'epsilon' in re]
        random.shuffle(complex_re_set)
        length = len(complex_re_set)
        valid_ratio = int(length * 0.15)
        test_ratio = int(length * 0.15)
        train_ratio = length - valid_ratio -test_ratio
        
        if length == 0:
            continue

        valid = complex_re_set[:valid_ratio]
        test = complex_re_set[valid_ratio:valid_ratio+test_ratio]
        train = complex_re_set[valid_ratio+test_ratio:]
        
        test_pair = [d + '\t' + simple_re for d in test]
        valid_pair = [d + '\t' + simple_re for d in valid]
        train_pair = [d + '\t' + simple_re for d in train]
        
        train_set.extend(train_pair)
        valid_set.extend(valid_pair)
        test_set.extend(test_pair)
    
    print('total data ratio train {} valid {} test {}'.format(len(train_set), len(valid_set), len(test_set)))
    
    with open('dataset/complex_simple_train.pickle', 'wb') as fw:
        pickle.dump(train_set, fw, pickle.HIGHEST_PROTOCOL)
    
    with open('dataset/complex_simple_valid.pickle', 'wb') as fw:
        pickle.dump(valid_set, fw, pickle.HIGHEST_PROTOCOL)
    
    with open('dataset/complex_simple_test.pickle', 'wb') as fw:
        pickle.dump(test_set, fw, pickle.HIGHEST_PROTOCOL)

        

with open('dataset/state_elimination_dataset/simple_regexs_dataset.pickle','rb') as rf:
    simple_re_se_pair = pickle.load(rf)

with open('dataset/state_elimination_dataset/complex_regexs_dataset.pickle','rb') as rf:
    complex_re_se_pair = pickle.load(rf)
    
merged_dataset = simple_re_se_pair + complex_re_se_pair
generating_train_valid_test(merged_dataset)
