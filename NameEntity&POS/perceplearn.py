import sys
import pickle
import argparse
import random
from copy import deepcopy
from collections import defaultdict

#Return a list that contain the correct labels of the development file
def DevCls(devfile):
    cls_list = []
    
    for line in devfile:
        words = line.split()
        cls_list.append(words[0])
    return cls_list
    
#Return the error rate getting by compare the correct labels and predicted labels 
#using model stored for each iteration 
def GetDevErrRate(dev_cls_list, model, devfile):
    result_cls = None
    err_rate = 0
    err_num = 0
    classify_list = []
    item_num = len(dev_cls_list)
    first_word = ''
    for word in model['words_cls_weight_map_dict'].keys():
        first_word = word
        break
    
    i = 0      
    for line in devfile:
        words = line.split()
        max_cls_weight_sum = -float('inf')
        result_cls = random.choice(list(model['class_weight_map_dict'].keys()))

        for cls in model['words_cls_weight_map_dict'][first_word].keys():
            cur_cls_weight_sum = 0
            for word in words:
                if word in model['words_cls_weight_map_dict'].keys():
                    cur_cls_weight_sum += model['words_cls_weight_map_dict'][word][cls]
                    
            if cur_cls_weight_sum > max_cls_weight_sum:
                max_cls_weight_sum = cur_cls_weight_sum
                result_cls = cls
        classify_list.append(result_cls)
        i += 1
    
    for i in range(0, item_num):
        if dev_cls_list[i] != classify_list[i]:
            err_num += 1
            
    err_rate = err_num / item_num
    return err_rate


def PercepLearn():
    #set argparser
    print('I am learning')
    parser = argparse.ArgumentParser(description='-------This is a description of %(prog)s)', epilog = '-------This is a epilog of %(prog)s', add_help=False)
    parser.add_argument('-h', dest='devfile', help='path of develop ment data file')
    parser.add_argument('input_path', help='path of legal formatted file as input')
    parser.add_argument('model_path', help='path of model file as output')
    parser.add_argument('-i', dest='iter_wanted', help='number of iteration for update the weights', type=int)
    args = parser.parse_args()
     
    has_devfile = False
    devfile = None
    dev_cls_list = []
    if args.devfile != None:
        has_devfile = True
        with open(args.devfile, 'r') as devfile:
            dev_cls_list = DevCls(devfile)


    input_file_path = args.input_path
    model_file_path = args.model_path
    iter_wanted = 20
    if args.iter_wanted != None:
        iter_wanted = args.iter_wanted

    #dict that map class to its weight, it is the value of each key word of words_cls_weight_map_dict
    class_weight_map_dict = {}
    #result dict to write in binary file for percepclassify use
    model_dict = {'class_weight_map_dict':{}, 'words_cls_weight_map_dict':{}}
    #dict contain word vocabulary as the keys, each value of a key is the weights of each class for this word
    words_cls_weight_map_dict = {}
    #dict that contain word vocabulary as keys, but the weight of each class for a word is the average weight
    avg_weight_dict = {}

    result_avg_weight_dict = {}

    min_err_rate = 1

    with open(input_file_path, 'r') as input_file:
    
        #set up class_weight_map_dict and get the total number of lines in input file
        line_cnt = 0
        for line in input_file:
            line_cnt += 1
            words = line.split()
            if words[0] not in class_weight_map_dict.keys():
                class_weight_map_dict[words[0]] = 0

        model_dict['class_weight_map_dict'] = class_weight_map_dict

        #if any weights is changed in the previous iteration, need more iteraton for the weight to the converge      
        more_iter = True;
        #num count for iterations
        iter_num = 0

        c = 1
        while(more_iter):
            #number of lines that revised their weight
            weight_revised = False;
            iter_num += 1
            if iter_num > iter_wanted:
                break

            with open(input_file_path, 'r') as input_file:
                lines = [line for line in input_file]
                random.shuffle(lines)
                num = 0
                for line in lines:
                    #for each iteration, store each line's words occurance in this dict
                    temp_word_occurance_dict = defaultdict(int)
                    words = line.split()
                    for i in range(1, len(words)):
                        #update the words' occurance in this line
                        temp_word_occurance_dict[words[i]] += 1
                        if words[i] not in words_cls_weight_map_dict:
                            #update the model_dict by adding a new word when it first occurs in this line
                            words_cls_weight_map_dict[words[i]] = deepcopy(class_weight_map_dict)
                            avg_weight_dict[words[i]] = deepcopy(class_weight_map_dict)  

                    #W(z).f(xi)
                    class_argmax_weight_sum = -float('inf')
                    #class with the largest weight sum

                    class_argmax = random.choice(list(class_weight_map_dict.keys()))
                    #the class in reality
                    real_class = words[0]
                    
                    for cls in class_weight_map_dict.keys():
                        cur_weight_sum = 0
                        for word in temp_word_occurance_dict.keys():
                            cur_weight_sum += words_cls_weight_map_dict[word][cls] * temp_word_occurance_dict[word]
                        #update to find class that argmax
                        if cur_weight_sum > class_argmax_weight_sum:
                            class_argmax = cls
                            class_argmax_weight_sum = cur_weight_sum
                    
                    #If predicted class is wrong, update the weights
                    if class_argmax != real_class:
                        for word in temp_word_occurance_dict.keys():
                            words_cls_weight_map_dict[word][class_argmax] -= temp_word_occurance_dict[word]
                            avg_weight_dict[word][class_argmax] -= c * temp_word_occurance_dict[word]
                            words_cls_weight_map_dict[word][real_class] += temp_word_occurance_dict[word]
                            avg_weight_dict[word][real_class] += c * temp_word_occurance_dict[word]
                            weight_revised = True;
                    
                c += 1
                
                #If provided the development file, collect the error rate for each iteration and store the 
                #iteration's average weights with smallest error rate
                if has_devfile:
                    with open(args.devfile, 'r') as devfile:
                        temp_avg_dict = deepcopy(avg_weight_dict)
                        for word in avg_weight_dict.keys():
                            for cls in avg_weight_dict[word].keys():
                                temp_avg_dict[word][cls] = words_cls_weight_map_dict[word][cls] - temp_avg_dict[word][cls] / c
      
                        model_dict['words_cls_weight_map_dict'] = temp_avg_dict
                        err_rate = GetDevErrRate(dev_cls_list, model_dict, devfile)
                        if err_rate < min_err_rate:
                            min_err_rate = err_rate
                            result_avg_weight_dict = deepcopy(temp_avg_dict)                           
                        if iter_num < 10:
                            print('iter'+str(iter_num)+'  devErr: '+str(err_rate))
                        else:
                            print('iter'+str(iter_num)+' devErr: '+str(err_rate))

                else:
                    result_avg_weight_dict = deepcopy(avg_weight_dict)
                    print('iter'+str(iter_num))
                
                #If no weights updated in this iteration, end iterate
                if weight_revised == False:
                    more_iter = False

        #If not provide the development file, get the final averaged weights
        if not has_devfile:
            for word in result_avg_weight_dict.keys():
                for cls in result_avg_weight_dict[word].keys():
                    result_avg_weight_dict[word][cls] = words_cls_weight_map_dict[word][cls] - result_avg_weight_dict[word][cls] / c

        model_dict['words_cls_weight_map_dict'] = result_avg_weight_dict 

        with open(model_file_path, 'wb') as model_file:      
            pickle.dump(model_dict, model_file, protocol = 2)
            
        #print('The smallest error rate is ' + str(min_err_rate))
        print('done') 


if __name__ == '__main__':
    PercepLearn()
