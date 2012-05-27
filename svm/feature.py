#!/usr/bin/env python
'''
We use the program to process DNA sequence.
We can input DNA sequence by a argment or standard input stream.
Carefully,one DNA sequence must be one line,each line is separated by '\n'
'''

import sys, getopt

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

def generate_3meta(dna_seq):
	meta = {}
	for i1 in 'atcg':
		for i2 in 'atcg':
			for i3 in 'atcg':
				meta[i1+i2+i3] = 0
	
	for i,val in enumerate(dna_seq):
		start = i
		end = start + 3

		if len(dna_seq[start:end]) < 3:
			break

		if meta.has_key(dna_seq[start:end]):
			meta[dna_seq[start:end]] += 1
		#else:
			#print dna_seq[start:end]
			#raise Exception,'Has unrecognized charactor in DNA sequnence'
	
	return meta.values()

#analyze dna data file,and return a feature matrix 
def analyze_dna_data(dna_seq_file):
	feature_matrix = []
	feature_vector = []

	for line in dna_seq_file:
		feature_vector = []

		line = line.strip()
		line = line.strip("\n")
		#generate DNA feature vector,and add to vector
		feature_vector += generate_base_rate(line)
		feature_vector += generate_dna_length(line)
		feature_vector += generate_3meta(line)

		feature_matrix.append(feature_vector)

	return feature_matrix

#generate a certain format feature vector with feature matrix
#we can free redirect standard output stream,such as a file
def generate_feature(feature_matrix, label, format = 'self'):
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

def usage(msg = None):
	if msg != None:
		print msg
		print 'Try `./feature.py -h` for more'
	else:
		print '''
usage: ./feature.py [options] class_indentify [DNA_sequence_file]
options:
-h for help,just this
-f set the format for output,(0 is self format,1 is libsvm format,default is 0)

example:
	./feature.py 1 DNA.data > feature.data
	'''

def main():
	param = {}
	param['formater'] = 'self'
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hf:')
	except getopt.GetoptError, msg:
		usage(msg)
		exit(1)
		
	for opt, val in opts:
		if opt == '-h':
			usage()
			exit()
		elif opt == '-f':
			if val == '0':
				param['formater'] = 'self'
			elif val == '1':
				param['formater'] = 'libsvm'
			else:
				usage('specified output format error')
				exit(1)


	try:
		if len(args) < 1:
			usage('Must specify classcify label')
			exit(1)
		elif len(args) < 2:
			file = sys.stdin
		else:
			file = open(args[1])
	except IOError,msg:
		usage(msg)
		exit(1)
	feature_matrix = []
	feature_matrix.extend(analyze_dna_data(file))
	generate_feature(feature_matrix, args[0], param['formater'])

if __name__ == '__main__':
	main()
