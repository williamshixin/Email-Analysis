import sys
import fnmatch
import os
import string

def result_generator(srcFile, feature, result):
    
    for line in srcFile:
        #words = line.split()
        no_punc = (''.join(word.strip(string.punctuation) for word in line)).split()
        for word in no_punc:
            feature += word + ' '
            
    result.write(feature + '\n' )

def file_format():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. format.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        try:
            result = open(output_path, "w")
            class_set = {()}
            
            #get all the classes in a set
            for file_name in os.listdir(input_path):
                
                file_name_words = file_name.split('.')
                
                if file_name_words[0] in class_set:
                    pass
                else:
                    class_set.add(file_name_words[0])
                    
            #for one file, put class and bag-in-wrods feature in one line       
            for file_name in sorted(os.listdir(input_path)):
                
                feature = ''
                src_file = open(input_path + '/' + file_name, 'r', errors = 'ignore')
                file_name_words = file_name.split('.')
                
                if fnmatch.fnmatch(file_name, file_name_words[0] + '.*'):
                    feature += file_name_words[0] + ' '
                    result_generator(src_file, feature, result)
                #can not match the class in the class set, return and report an error
                else:
                    print('Error: file class can not match into the known class set, formating stop with this error!\n')
                    break
                
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")
        except OSError as e:
            print("Error: {}".format(e.strerror) + "\n")
            
if __name__ == '__main__':
    file_format()
