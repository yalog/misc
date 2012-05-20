#!/usr/bin/env python
import sys

'''
These file is writed by wangyalong
need to be more robus
'''

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

	for line in open(dna_seq_file):
		feature_vector = []

		#generate DNA feature vector,and add to vector
		feature_vector += generate_base_rate(line)
		feature_vector += generate_dna_length(line)

		feature_matrix.append(feature_vector)

	return feature_matrix

#normalize feature matrix,here using min-max method
def normalize_feature_matrix(feature_matrix):
	normalized_matrix = []
	max = 0
	min = 0
	
	for i in range(len(feature_matrix[0])):
		max = feature_matrix[0][i]
		min = feature_matrix[0][i]
		#find max and min value in a dim
		for j in range(len(feature_matrix)):
			if feature_matrix[j][i] > max:
				max = feature_matrix[j][i]
			if feature_matrix[j][i] < min:
				min = feature_matrix[j][i]

		#normalize the dim
		for j in range(len(feature_matrix)):
			try:
				feature_matrix[j][i] = (float(feature_matrix[j][i]) - min) / (max - min)
			except ZeroDivisionError:
				feature_matrix[j][i] = 0

	return feature_matrix

#generate a certain formate feature vector file with feature matrix
def generate_feature_file(feature_matrix, label, format = 'self'):

	if format == 'libsvm':
		fromater = libsvm_format
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
		
def exit_with_help():
	print """
usage: ./feature.py class_indentify dna_seq_file
	"""
	exit(1)

def main():
	if len(sys.argv) < 3:
		exit_with_help()
	
	class_indent = sys.argv[1]
	dna_seq_file = sys.argv[2]
	feature_matrix = []

	feature_matrix.extend(analyze_dna_data(dna_seq_file))
	#may need normalize feature
	feature_matrix = normalize_feature_matrix(feature_matrix)
	generate_feature_file(feature_matrix, class_indent)
main()
