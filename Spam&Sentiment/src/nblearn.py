import sys
import json
import math
import pickle

def nblearn():

    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. nblearn.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        try:
            formatted_files = open(input_path, 'r')
            '''learn_result_word_freq = open("/home/william/Documents/csci544_hw1/part1/learn_result_word_freq", 'w')
            learn_result_prob = open("/home/william/Documents/csci544_hw1/part1/learn_result_prob", 'w')'''
            prob = open(output_path, 'wb')

            total_tokens = 0
            vocab_size = 0
            total_file_num = 0
            #dictionary contains the occurance frequency of each class in all the files
            class_freq_cnt_dict = {}
            #dictrionary contains the occurance frequency of each word in all the files
            word_freq_cnt_dict = {}
            #dictrionary contains the occurance frequency of each word in all the files of each class
            word_in_class_freq_cnt_dict = {}
            #dictionary contains the probabilities of each class--P(ci)
            class_prob_dict = {}
            #dictionary contains the probabilities of each word in each class--P(wi/ci)
            word_prob_dict = {}
            #dictionary contains the probability of an unknown word in each class
            unknown_prob_dict = {}

            for line in formatted_files:

                words = line.split();
                #calculate the occurance of a class	
                if words[0] in class_freq_cnt_dict:
                    class_freq_cnt_dict[words[0]] += 1
                else:
                    class_freq_cnt_dict[words[0]] = 1

                for i in range(1, len(words)):
                    total_tokens += 1

                #calculate occurance of each word in a line for a class
                    if words[i] in word_freq_cnt_dict:
                        if words[0] in word_freq_cnt_dict[words[i]]:		
                            word_freq_cnt_dict[words[i]][words[0]] += 1
                        else:
                            word_freq_cnt_dict[words[i]][words[0]] = 1
                    else:
                        word_freq_cnt_dict[words[i]] = {words[0]:1}

                #initialize dict of word probabilities
                    if words[i] in word_prob_dict:
                        if words[0] in word_prob_dict[words[i]]:
                            pass
                        else:
                            word_prob_dict[words[i]][words[0]] = 0
                    else:
                         word_prob_dict[words[i]] = {words[0]:0}
 
            #calculate the probability of each word in each class
            vocab_size = len(word_freq_cnt_dict.keys())
    
            #initialize word_in_class_freq_cnt_dict
            for class_key in class_freq_cnt_dict.keys():
                word_in_class_freq_cnt_dict[class_key] = 0

            #calculate the token size of each class
            for word_key in word_freq_cnt_dict.keys():
                for class_key in word_freq_cnt_dict[word_key].keys():
                    word_in_class_freq_cnt_dict[class_key] += word_freq_cnt_dict[word_key][class_key]
    
            for word_key in word_prob_dict.keys():

                for class_key in class_freq_cnt_dict.keys():
                    denominator = word_in_class_freq_cnt_dict[class_key] + vocab_size
                    if class_key in word_freq_cnt_dict[word_key]:
                        prob_in_log = math.log((word_freq_cnt_dict[word_key][class_key] + 1)/ denominator)
                    else:
                        prob_in_log = math.log(1 / denominator)
                    word_prob_dict[word_key][class_key] = prob_in_log

            #calculate the probability of each p(c) 
            keys_class_freq_dict = class_freq_cnt_dict.keys()
            for item in keys_class_freq_dict:
                total_file_num += class_freq_cnt_dict[item]
    
            for item in keys_class_freq_dict:
                class_prob_dict[item] = math.log(class_freq_cnt_dict[item] / total_file_num)
    
            #calculate the probability of unknown words
            for class_key in class_freq_cnt_dict.keys():
                unknown_prob_dict[class_key] = math.log(1 / (word_in_class_freq_cnt_dict[class_key] + vocab_size + 1))

            prob_dict = {'class_prob':class_prob_dict, 'word_prob':word_prob_dict, 'unknown_prob':unknown_prob_dict}
    
            '''print(vocab_size)
            print(word_in_class_freq_cnt_dict)
            print(class_prob_dict)
            print(unknown_prob_dict)'''
            '''learn_result_word_freq.write(json.dumps(word_freq_cnt_dict, sort_keys = True, indent = 1))
            learn_result_prob.write(json.dumps(word_prob_dict,sort_keys = True, indent = 1))'''
            pickle.dump(prob_dict, prob, protocol = 2)
        
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")

if __name__ == '__main__':
    nblearn()


