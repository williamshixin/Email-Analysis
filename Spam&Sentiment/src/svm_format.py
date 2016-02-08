import sys
import fnmatch
import os
import pickle
import math
import string
def svm_format():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. format.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        try:
            result = open(output_path, "w")
            index_dict = open("/home/william/Documents/csci544_hw1/part2/index_dict.svm", 'rb')
            #dict contains words map to indices for svmlight
            word_index_map_dict = pickle.load(index_dict)

            unknown_index = len(word_index_map_dict.keys()) + 1
            unknown_map_dict = {unknown_index:0}
            #dict contains indices frequency pairs
            index_freq_dict = {}
            unknown_freq_dict = {unknown_index:0}
            class_label_map_dict = {'SPAM':'+1', 'HAM':'-1', 'POS':'+1', 'NEG':'-1'}
            class_word_freq_dict = {'-1':0, '+1':0}
            word_in_class_freq_dict = {}
            
            '''i = 1
            
            for file_name in sorted(os.listdir(input_path)):
                file_name_words = file_name.split('.')
                
                src_file = open(input_path + '/' + file_name, 'r', errors = 'ignore')
                #src_file = open(input_path + '/' + file_name, 'r')
                for line in src_file:
                    words = line.split()
                    for word in words:
                        if word not in word_in_class_freq_dict:
                            word_in_class_freq_dict[word] = {file_name_words[0]:1}
                        else:
                            if file_name_words[0] not in word_in_class_freq_dict[word]:
                                word_in_class_freq_dict[word][file_name_words[0]] = 1
                            else:
                                word_in_class_freq_dict[word][file_name_word[0]] += 1
                                
                        class_word_freq_dict[class_label_map_dict[file_name_words[0]]] += 1
                        
                        if word not in word_index_map_dict:
                            word_index_map_dict[word] = i
                            i += 1'''
            #dicts = open("/home/william/Documents/csci544_hw1/part2/ddddd", 'w')
            #dicts.write(word_index_map_dict)
            #json.dumps(word_index_map_dict, dicts, indent = 1)
            #print(len(word_index_map_dict.keys()))
            for index in range(1, len(word_index_map_dict.keys()) + 1):
                index_freq_dict[index] = 0
            #print(len(word_index_map_dict.keys()))    
            #for one file, put class and bag-in-wrods feature in one line       
            for file_name in sorted(os.listdir(input_path)):
                if fnmatch.fnmatch(input_path, 'SPAM_training') or fnmatch.fnmatch(input_path, 'SENTIMENT_training') or fnmatch.fnmatch(input_path, 'SPAM_dev') or fnmatch.fnmatch(input_path, 'SENTIMENT_training2000')or fnmatch.fnmatch(input_path, 'SENTIMENT_training23000') :
                    file_name_words = file_name.split('.')
                
                    feature = class_label_map_dict[file_name_words[0]] + ' '
                else:
                    feature = '-1' + ' '


                #total_in_class = class_word_freq_dict[class_label_map_dict[file_name_words[0]]]
                
                src_file = open(input_path + '/' + file_name, 'r', errors = 'ignore')

                local_index_freq_dict = index_freq_dict.copy()
                local_unknown_freq_dict = unknown_freq_dict.copy()
                
                word_cnt = 0
                
                for line in src_file:
                    words = line.split()
                    #no_punc = (''.join(word.strip(string.punctuation) for word in line)).split()
                    #word_cnt += len(no_punc)
                    word_cnt += len(words)
                    for word in words:
                        if word in word_index_map_dict:
                            index = word_index_map_dict[word]
                            local_index_freq_dict[index] += 1
                        else:
                            local_unknown_freq_dict[unknown_index] += 1
                
                for index in range(1, len(word_index_map_dict.keys()) + 1):
                    if local_index_freq_dict[index] != 0:
                        feature += str(index) + ':' + str(local_index_freq_dict[index] / word_cnt) + ' '
                        
                if local_unknown_freq_dict[unknown_index] != 0:
                    feature += str(unknown_index) + ':' + str(local_unknown_freq_dict[unknown_index] / word_cnt)
                
                result.write(feature + '\n' )

                
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")
        except OSError as e:
            print("Error: {}".format(e.strerror) + "\n")
            
if __name__ == '__main__':
    svm_format()
