import sys
import fnmatch
import os
import pickle
import math
import string
def megam_format():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. megam_format.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        try:
            result = open(output_path, "w")
            class_label_map_dict = {'SPAM':'1', 'HAM':'0', 'POS':'1', 'NEG':'0'}
            '''class_word_freq_dict = {'0':0, '1':0}'''
    
            for file_name in sorted(os.listdir(input_path)):
                if input_path == 'SPAM_training' or input_path == 'SPAM_dev' or input_path == 'SENTIMENT_training' or input_path == 'SENTIMENT_training2000' or input_path == 'SENTIMENT_training23000':
                    file_name_words = file_name.split('.')
                    feature = class_label_map_dict[file_name_words[0]] + ' '
                else:
                    feature = '0' + ' '
                    
                src_file = open(input_path + '/' + file_name, 'r', errors = 'ignore')

                feature_dict = {}
                '''word_cnt = 0'''
                for line in src_file:

                    no_punc = (''.join(word.strip(string.punctuation) for word in line)).split()
                    '''word_cnt += len(no_punc)'''
                    for word in no_punc:
                        if word in feature_dict:
                            feature_dict[word] += 1
                        else:
                            feature_dict[word] = 1
                
                for item in feature_dict.keys():
                        feature += item + ' ' + str(1.0) + ' '
                
                result.write(feature + '\n' )

                
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")
        except OSError as e:
            print("Error: {}".format(e.strerror) + "\n")
            
if __name__ == '__main__':
    megam_format()
