import sys
import argparse
import pickle

def modelGen():
	
	parser = argparse.ArgumentParser(description='-------This is a description of %(prog)s', \
		epilog='-------This is a epilog of %(prog)s')
	parser.add_argument('raw_model', help='This is the path of the raw model for processing as input')
	parser.add_argument('model', help='This is the path of model file as output')
	args = parser.parse_args()

	input_path = args.raw_model
	output_path = args.model

	uni_gram_dict = {}
	bi_gram_dict = {}
	tri_gram_dict = {}
	ngram_dict = {'1-grams':uni_gram_dict, '2-grams':bi_gram_dict, '3-grams':tri_gram_dict}

	uni_gram_total = 0
	bi_gram_total = 0
	tri_gram_total = 0
	uni_gram_cnt = 0
	bi_gram_cnt = 0
	tri_gram_cnt = 0

	update_uni_gram = False
	update_bi_gram = False
	update_tri_gram = False

	with open(input_path, 'r') as input_file:
		for line in input_file:
			words = line.split()

			if len(words) > 0:
				if words[0] == 'ngram':
					w = words[1].split('=')
					if w[0] == '1':
						uni_gram_total = int(w[1])
					elif w[0] == '2':
						bi_gram_total = int(w[1])
					elif w[0] == '3':
						tri_gram_total = int(w[1])
				elif words[0] == '\\1-grams:':
					update_uni_gram = True
				elif words[0] == '\\2-grams:':
					update_bi_gram = True
				elif words[0] == '\\3-grams:':
					update_tri_gram = True

				if update_uni_gram and len(words) > 1:
					if words[1] not in uni_gram_dict.keys():
						uni_gram_dict[words[1]] = {'prob':float(words[0]), 'backoff':float(words[2])}
					uni_gram_cnt += 1

				if update_bi_gram and len(words) > 1:
					bi_gram_key = words[1] + ' ' + words[2]
					if bi_gram_key not in bi_gram_dict.keys():
						bi_gram_dict[bi_gram_key] = {'prob':float(words[0]), 'backoff':float(words[3])}
					bi_gram_cnt += 1

				if update_tri_gram and len(words) > 1:
					tri_gram_key = words[1] + ' ' + words[2] + ' ' + words[3]
					if tri_gram_key not in tri_gram_dict.keys():
						tri_gram_dict[tri_gram_key] = float(words[0])
					tri_gram_cnt += 1

				if uni_gram_cnt == uni_gram_total:
					update_uni_gram = False

				if bi_gram_cnt == bi_gram_total:
					update_bi_gram = False

				if tri_gram_cnt == tri_gram_total:
					update_tri_gram = False

	with open(output_path, 'wb') as output_file:
		pickle.dump(ngram_dict, output_file, protocol=2)

if __name__ == '__main__':
	modelGen()