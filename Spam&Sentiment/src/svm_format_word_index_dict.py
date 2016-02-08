import sys
import fnmatch
import os
import pickle
import string
import json
def svm_format_get_dict():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. format.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        

        try:
            
            result = open(output_path, "wb")
            
            word_index_map_dict = {}
            
            i = 1

            for file_name in sorted(os.listdir(input_path)):
                file_name_words = file_name.split('.')
                
                src_file = open(input_path + '/' + file_name, 'r', errors = 'ignore')
                #src_file = open(input_path + '/' + file_name, 'r')
                for line in src_file:
                    words = line.split()
                    #no_punc = (''.join(word.strip(string.punctuation) for word in line)).split()
                    
                    for word in words:
                        
                        if word not in word_index_map_dict:
                            word_index_map_dict[word] = i
                            i += 1
                            
            pickle.dump(word_index_map_dict, result, protocol = 2)

                
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")
        except OSError as e:
            print("Error: {}".format(e.strerror) + "\n")
            
if __name__ == '__main__':
    svm_format_get_dict()
