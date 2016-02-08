import sys
sys.path.append('../')
#import locale
import argparse
#import subprocess
from perceplearn import PercepLearn
import sys
import re

DEV_FORMATTED_FILENAME = 'ner_dev_formatted.temp'
INPUT_FORMATTED_FILENAME = 'ner_input_formatted.temp'

def getWshape(word):
    word = re.sub('[a-z]+', 'a', word)
    word = re.sub('[A-Z]+', 'A', word)
    word = re.sub('[0-9]+', '9', word)
    word = re.sub('[^0-9a-zA-Z]+', '-',word)
    return word

def InputFormat(input_path, dev_or_input):
    temp_file = DEV_FORMATTED_FILENAME

    if dev_or_input:
        temp_file = INPUT_FORMATTED_FILENAME
        print('Formatting development file...')
    else:
        print('Formatting input file...')

    with open(temp_file, 'w') as ner_formatted_file:
        with open(input_path, 'r', encoding='latin-1',errors='ignore') as input_file:
            for line in input_file:
                words_and_tags = line.split()
                words_and_tags.insert(0, 'BOS/BOS/O')
                words_and_tags.append('EOS/EOS/O')
                for i in range(1, len(words_and_tags) - 1):
                    formatted_line = ''
                    word_tag_pair = words_and_tags[i].split('/')
                    word = word_tag_pair[0]
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
                    pos = word_tag_pair[1]
                    tag = word_tag_pair[2]
                    prew = words_and_tags[i-1].split('/')[0]
                    pre_ner = words_and_tags[i-1].split('/')[2]
                    next_word = words_and_tags[i+1].split('/')[0]
                    formatted_line = tag + ' ' + 'pre:' + pre_ner + ' ' + 'pos:' + pos + ' ' + 'prew:'+prew+' '+'w:' + word + ' ' + 'next:' + next_word + ' ' + 'wshape:' + wshape + ' ' + 'surfix2:' + surfix2 + ' ' + 'surfix3:' + surfix3 + '\n'
                    ner_formatted_file.write(formatted_line)



def PosTrain():
    #set argparser
    parser = argparse.ArgumentParser(description='-------This is a description of %(prog)s)', epilog = '-------This is a epilog of %(prog)s', add_help=False)
    parser.add_argument('-h', dest='devfile', help='path of development data file')
    parser.add_argument('input_path', help='path of legal formatted file as input')
    parser.add_argument('model_path', help='path of model file as output')
    parser.add_argument('-i', dest='iter_wanted', help='number of iteration for update the weights', type=int)
    args = parser.parse_args()

    input_file_path = args.input_path
    model_file_path = args.model_path

    for i in range(0, len(sys.argv)):
        if sys.argv[i] == input_file_path:
            sys.argv[i] = INPUT_FORMATTED_FILENAME
        if args.devfile != None:
            if sys.argv[i] == args.devfile:
                sys.argv[i] = DEV_FORMATTED_FILENAME

    InputFormat(input_file_path, True)

    if args.devfile != None:
        InputFormat(args.devfile, False)

    print('Begin learning...')
    PercepLearn()

if __name__ == '__main__':
	PosTrain()