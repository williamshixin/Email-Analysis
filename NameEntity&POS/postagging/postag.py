import sys
import pickle
import argparse
from copy import deepcopy
from sys import stdin
import re

def getWshape(word):
    word = re.sub('[a-z]+', 'a', word)
    word = re.sub('[A-Z]+', 'A', word)
    word = re.sub('[0-9]+', '9', word)
    word = re.sub('[^0-9a-zA-Z]+', '-',word)
    return word

def PosTag():

    parser = argparse.ArgumentParser(description='-------This is a description of %(prog)s', epilog = '-------This is a epilog of %(prog)s')
    parser.add_argument('model_path', help='path of model file')
    args = parser.parse_args()
      
    model_file_path = args.model_path
    
    with open(model_file_path, 'rb') as model_file:
        model = pickle.load(model_file)
        first_word = ''
        for word in model['words_cls_weight_map_dict'].keys():
            first_word = word
            break
        
        for cls in model['class_weight_map_dict'].keys():
            default_class = cls
            break
        
        for line in stdin:
            output_line = ''
            l = []
            result_tag_list = []
            words = line.split()
            word_list = deepcopy(words)
            words.insert(0, 'BOS')
            words.append('EOS')
            for i in range(1, len(words) - 1):
                formatted_line = ''
                word = words[i]
                wshape = getWshape(word)
                surfix2 = ''
                surfix3 = ''
                if len(word) >= 2:
                    surfix2 = word[len(word)-2] + word[len(word)-1]
                else:
                    surfix2 = word
                if len(word) >= 3:  
                    surfix3 = word[len(word)-3] + word[len(word)-2] + word[len(word)-1]
                else:
                    surfix3 = word
                pre_word = words[i-1]
                next_word = words[i+1]
                formatted_line = 'pre:' + pre_word + ' ' + 'w:' + word + ' ' + 'next:' + next_word + ' ' + 'wshape:' + wshape + ' ' + 'surfix2:' + surfix2 + ' ' + 'surfix3:' + surfix3
                l.append(formatted_line)

            for item in l:
                max_cls_weight_sum = -float('inf')
                result_cls = default_class

                for cls in model['words_cls_weight_map_dict'][first_word].keys():
                    cur_cls_weight_sum = 0

                    for word in item.split():
                        if word in model['words_cls_weight_map_dict'].keys():
                            cur_cls_weight_sum += model['words_cls_weight_map_dict'][word][cls]
                    
                    if cur_cls_weight_sum > max_cls_weight_sum:
                        max_cls_weight_sum = cur_cls_weight_sum
                        result_cls = cls  
                result_tag_list.append(result_cls)
            for cnt in range(0, len(word_list)):
                output_line += word_list[cnt] + '/' + result_tag_list[cnt] + ' '
            print(output_line)  
            sys.stdout.flush()   


if __name__ == '__main__':
    PosTag()