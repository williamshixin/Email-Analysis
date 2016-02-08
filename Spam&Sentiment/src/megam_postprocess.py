import sys

def megam_postprocess():
    
    arg_num = sys.argv
    
    if  len(arg_num) != 3:
        print("Error! Must have 3 argements: script name, input file name and output file name.\nE.g. svm_postprocess.py ~/Desktop/input ~/Desktop/output\n")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        try:
            result = open(output_path, "w")
            raw_result = open(input_path, 'r')
            file_name_words = input_path.split('.')
            
            for line in raw_result:
                words = line.split()
                if file_name_words[0] == 'spam':
                    if words[0] == '0':
                        result.write('HAM' + '\n')
                    else:
                        result.write('SPAM' + '\n')
                else:
                    if words[0] == '0':
                        result.write('NEG' + '\n')
                    else:
                        result.write('POS' + '\n')
             
        except IOError as e:
            print("Error: {}".format(e.strerror) + "\n")
        except OSError as e:
            print("Error: {}".format(e.strerror) + "\n")
            
if __name__ == '__main__':
    megam_postprocess()