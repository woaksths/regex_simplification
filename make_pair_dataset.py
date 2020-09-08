import random 
import pickle

def filewrite(dataset, fname):
    print(len(dataset), fname)
    with open(fname ,'w') as fw:
        for idx,data in enumerate(dataset):
            if idx == len(dataset)-1:
                fw.write(data)
            else:
                fw.write(data +'\n')

                
def preprocessing(string):                
    string = [char for char in string]
    return ' '.join(string)
                
                
def generating_train_valid_test(pair_dataset):
    train_set = []
    valid_set = []
    test_set = []
    
    for idx, data in enumerate(pair_dataset):
        simple_re = data['origin']
        complex_re_set = [complex_re for complex_re in list(data['complex'])\
                          if len(complex_re)>= len(simple_re) and complex_re != simple_re]

        length = len(complex_re_set)
        if length == 0:
            continue
        
        valid_ratio = int(length * 0.1)
        test_ratio = int(length * 0.1)
        train_ratio = length - valid_ratio -test_ratio
        
        valid = complex_re_set[:valid_ratio]
        test = complex_re_set[valid_ratio:valid_ratio+test_ratio]
        train = complex_re_set[valid_ratio+test_ratio:]
        
        
        test_pair = [preprocessing(d) + '\t' + preprocessing(simple_re) for d in test]
        valid_pair = [preprocessing(d) + '\t' + preprocessing(simple_re) for d in valid]
        train_pair = [preprocessing(d) + '\t' + preprocessing(simple_re) for d in train]
        
        train_set.extend(train_pair)
        valid_set.extend(valid_pair)
        test_set.extend(test_pair)

    print('total data ratio train {} valid {} test {}'\
          .format(len(train_set), len(valid_set), len(test_set)))
    
    filewrite(train_set, 'dataset/train.txt')
    filewrite(valid_set, 'dataset/valid.txt')
    filewrite(test_set, 'dataset/test.txt')



with open('dataset/state_elimination/star_height0_regexs_dataset.pickle','rb') as rf:
    star_height0_pair =  pickle.load(rf)
    star_height0_pair = [d for d in star_height0_pair if d is not None and isinstance(d,dict)]
    
with open('dataset/state_elimination/star_height1_regexs_dataset.pickle','rb') as rf:
    star_height1_pair =  pickle.load(rf)
    star_height1_pair = [d for d in star_height1_pair if d is not None and isinstance(d,dict)]

with open('dataset/state_elimination/star_height2_regexs_dataset.pickle','rb') as rf:
    star_height2_pair =  pickle.load(rf)
    star_height2_pair = [d for d in star_height2_pair if d is not None and isinstance(d,dict)]

print(len(star_height0_pair),len(star_height1_pair),len(star_height2_pair))
dataset = star_height0_pair + star_height1_pair + star_height2_pair
print(len(dataset))

generating_train_valid_test(dataset)
