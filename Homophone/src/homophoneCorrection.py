import sys
import argparse
import pickle
import re
import string
from sys import stdin

def homoReplace(wrong_word, right_word):
	w = wrong_word
	nopunc = re.sub('[!@#():;\",.?]', '', wrong_word)
	if len(nopunc) != len(w):
		pre_punc = ''
		sur_punc = ''
		for i in range(0, len(w)):
			if not w[i].isalpha():
				pre_punc += w[i]
			else:
				break
		j = -1
		while(j > -len(w)):
			if not w[j].isalpha():
				sur_punc += w[j]
			else:
				break
			j -= 1
		return pre_punc + right_word + sur_punc
	else:
		return right_word

def homoCorrecter():
	parser = argparse.ArgumentParser(description='-------This is a description of %(prog)s', \
		epilog='-------This is a epilog of %(prog)s')
	parser.add_argument('model_file', help='This is the model file path')
	args = parser.parse_args()

	model_path = args.model_file
	target_dict = {'it\'s': 'its', 'its': 'it\'s', 'you\'re': 'your', 'your': 'you\'re',\
		'they\'re': 'their', 'their': 'they\'re', 'loose': 'lose', 'lose': 'loose',\
		'to': 'too', 'too': 'to', 'It\'s': 'Its', 'Its': 'It\'s', 'You\'re': 'Your', 'Your': 'You\'re',\
		'They\'re': 'Their', 'Their': 'They\'re', 'Loose': 'Lose', 'Lose': 'Loose',\
		'To': 'Too', 'Too': 'To'} 
	model = None

	with open(model_path, 'rb') as model_file:
		model = pickle.load(model_file)

	for line in stdin:
		words = line.split()
		if(len(words) > 0):
			words.insert(0, '<s>')
			words.insert(0,'<s>')
			words.append('</s>')
			words.append('</s>')
			for i in range(2, len(words)-2):
				prew1 = re.sub('[!@#():;\",.?]', '', words[i-1]).lower()
				prew2 = re.sub('[!@#():;\",.?]', '', words[i-2]).lower()
				w = re.sub('[!@#():;\",.?]', '', words[i])
				nextw1 = re.sub('[!@#():;\",.?]', '', words[i+1]).lower()
				nextw2 = re.sub('[!@#():;\",.?]', '', words[i+1]).lower()
				if w in target_dict.keys():
					str1 = prew2 + ' ' + prew1 + ' ' + w
					str2 = w + ' ' + nextw1 + ' ' + nextw2
					prob1 = 0
					prob2 = 0

					if str1 in model['3-grams'].keys():
						prob1 = model['3-grams'][str1]
					elif prew1 + ' ' + w in model['2-grams'].keys():
						prob1 = model['2-grams'][prew1 + ' ' + w]['prob'] \
						 + model['2-grams'][prew1 + ' ' + w]['backoff']
					elif w in model['1-grams'].keys():
						prob1 = model['1-grams'][w]['prob'] \
						 + model['1-grams'][w]['backoff'] * 5

					if str2 in model['3-grams'].keys():
						prob2 = model['3-grams'][str2]
					elif w + ' ' + nextw1 in model['2-grams'].keys():
						prob2 = model['2-grams'][w + ' ' + nextw1]['prob']\
						 + model['2-grams'][w + ' ' + nextw1]['backoff']
					elif w in model['1-grams'].keys():
						prob2 = model['1-grams'][w]['prob'] + model['1-grams'][w]['backoff'] * 5

					str3 = prew2 + ' ' + prew1 + ' ' + target_dict[w]
					str4 = target_dict[w] + ' ' + nextw1 + ' ' + nextw2
					prob3 = 0
					prob4 = 0

					if str3 in model['3-grams'].keys():
						prob3 = model['3-grams'][str3]
					elif prew1 + ' ' + target_dict[w] in model['2-grams'].keys():
						prob3 = model['2-grams'][prew1 + ' ' + target_dict[w]]['prob'] \
						 + model['2-grams'][prew1 + ' ' + target_dict[w]]['backoff']
					elif target_dict[w] in model['1-grams'].keys():
						prob3 = model['1-grams'][target_dict[w]]['prob'] \
						 + model['1-grams'][target_dict[w]]['backoff'] * 5

					if str4 in model['3-grams'].keys():
						prob4 = model['3-grams'][str4]
					elif target_dict[w] + ' ' + nextw1 in model['2-grams'].keys():
						prob4 = model['2-grams'][target_dict[w] + ' ' + nextw1]['prob']\
						 + model['2-grams'][target_dict[w] + ' ' + nextw1]['backoff']
					elif target_dict[w] in model['1-grams'].keys():
						prob4 = model['1-grams'][target_dict[w]]['prob'] + model['1-grams'][target_dict[w]]['backoff'] * 5

					if prob1 < prob3 and prob1 + prob2 < prob3 + prob4:
						words[i] = homoReplace(words[i], target_dict[w])
					
		output_str = ''
		for i in range(2, len(words)-2):
			output_str += words[i] + ' '
		output_str.rstrip()
		print(output_str)

if __name__ == '__main__':
	homoCorrecter()