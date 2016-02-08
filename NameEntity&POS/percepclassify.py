import sys
import pickle
import argparse
from sys import stdin
from collections import defaultdict

def PercepClassify():

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
            words = line.split()
            max_cls_weight_sum = -float('inf')
            result_cls = default_class

            for cls in model['words_cls_weight_map_dict'][first_word].keys():
                cur_cls_weight_sum = 0

                for word in words:
                    if word in model['words_cls_weight_map_dict'].keys():
                        cur_cls_weight_sum += model['words_cls_weight_map_dict'][word][cls]
                if cur_cls_weight_sum > max_cls_weight_sum:
                    max_cls_weight_sum = cur_cls_weight_sum
                    result_cls = cls

            print(result_cls)    
            sys.stdout.flush()    


if __name__ == '__main__':
    PercepClassify()
