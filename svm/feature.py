#!/usr/bin/env python
'''
We use the program to process DNA sequence.
We can input DNA sequence by a argment or standard input stream.
Carefully,one DNA sequence must be one line,each line is separated by '\n'
'''

import sys

#These are the functions for generate feature vector vale by DNA sequence
def generate_base_rate(dna_seq):
	vector = []
	dna = dna_seq.lower()
	vector += [dna.count('a')]
	vector += [dna.count('g')]
	vector += [dna.count('c')]
	vector += [dna.count('t')]

	return vector

def generate_dna_length(dna_seq):
	vector = []
	vector += [len(dna_seq)]

	return vector

#analyze dna data file,and return a feature matrix 
def analyze_dna_data(dna_seq_file):
	feature_matrix = []
	feature_vector = []

	for line in dna_seq_file:
		feature_vector = []

		#generate DNA feature vector,and add to vector
		feature_vector += generate_base_rate(line)
		feature_vector += generate_dna_length(line)

		feature_matrix.append(feature_vector)

	return feature_matrix

#generate a certain format feature vector with feature matrix
#we can free redirect standard output stream,such as a file
def generate_feature(feature_matrix, label, format = 'libsvm'):
	if format == 'libsvm':
		formater = libsvm_format
	elif format == 'self':
		formater = self_format
	else:
		raise Exception, 'SVM data format seted error'

	for vector in feature_matrix:
		print "%s%s"%(label,formater(vector))

def libsvm_format(vector):
	str = ''
	index = 1

	for value in vector:
		str += " %d:%g"%(index, value)
		index += 1

	return str

def self_format(vector):
	str = ''

	for value in vector:
		str += " %g"%(value)

	return str

def usage():
	print '''
usage: ./feature.py -h | class_indentify [DNA_sequence_file]
example:
	./feature.py 1 DNA.data > feature.data
	'''

def main():
	if len(sys.argv) < 2:
		usage()
		exit(1)
	elif sys.argv[1] == '-h':
		usage()
		exit(0)
	else:
		try:
			if len(sys.argv) < 3:
				file = sys.stdin
			else:
				file = open(sys.argv[2])
		except IOError,msg:
			print msg
			exit(1)
	
	feature_matrix = []
	feature_matrix.extend(analyze_dna_data(file))
	generate_feature(feature_matrix, sys.argv[1])

if __name__ == '__main__':
	main()
