import sys
import pickle
import os
import string

def nbclassify():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. nbclassify.py ~/Desktop/input ~/Desktop/output\n")
    else:
        
        model_file_path = sys.argv[1]
        dir_path = sys.argv[2]
        input_file_words = model_file_path.split('.')
        output_path = '/home/william/Documents/csci544_hw1/' + input_file_words[0] + '.out'
        classified_prob = {}
        
        try:
            prob_file = open(model_file_path, "rb")
            model = pickle.load(prob_file)
            outputf = open(output_path, "w")
            
            for file_name in sorted(os.listdir(dir_path)):
                
                #format the input files
                feature = ''
                src_file = open(dir_path + '/' + file_name, 'r', errors = 'ignore')
                for line in src_file:
                        #words = line.split()
                        no_punc = (''.join(word.strip(string.punctuation) for word in line)).split()
                        for word in no_punc:
                            feature += word + ' '
                
                #
                feature_list = feature.split()
                classes = model['class_prob'].keys()
                for item in classes:
                    prob = model['class_prob'][item]
                    for f in feature_list:
                        if f in model['word_prob']:
                            if item in model['word_prob'][f]:
                                prob += model['word_prob'][f][item]
                        else:
                            prob += model['unknown_prob'][item]
                    classified_prob[item] = prob
                
                #print(keys_in_classified_prob)
                max_prob = -float('inf')
                result_class = ''
                
                for i in classified_prob.keys():
                    if classified_prob[i] > max_prob:
                        max_prob = classified_prob[i]
                        result_class = i
                        
                print(result_class)
                outputf.write(result_class + '\n')
                
        except IOError as e:
                    print("IOError: {}".format(e.strerror) + "\n")
        except OSError as e:
                    print("OSError: {}".format(e.strerror) + "\n")
                    
if __name__ == '__main__':
    nbclassify()
