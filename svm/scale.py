#!/usr/bin/env python
'''
The program is used to scale feature data(orignal training data).
Before scaling,We must put all feature data into one file
'''
import sys, getopt

def load_sample(feature_file):
	feature = {'target':[], 'matrix':[]}

	for line in feature_file:
		if line.startswith('#'):
			continue

		line = line.strip()
		line = line.strip("\n") #may can not work in across defferent OS
		fields = line.split(' ')#in default,space is used to split
		feature['target'].append(int(fields.pop(0)))
		fields = map(lambda x:float(x), fields)
		feature['matrix'].append(fields)

	return feature

def save_sample(target, feature_matrix):
	str = ''

	for i, v in enumerate(target):
		str = "%d"%(v)
		for j in feature_matrix[i]:
			str += " %g"%(j)

		print str

#normalize feature matrix,here using min-max method
def normalize_feature_matrix(feature_matrix):
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

def usage(msg = None):
	if msg != None:
		print msg
		print 'Try `./scale.py -h` for more'
	else:
		print '''
usage:./scale.py [options] [unnormalize_feature_file]
options:
-h for help,just this

example:
	./scale.py feature.data > scale_feature.data
	'''

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'h')
	except getopt.GetoptError, msg:
		usage(msg)
		exit(1)
	
	for opt, val in opts:
		if opt == '-h':
			usage()
			exit()
	
	try:
		if len(args) > 0:
			file = open(args[0])
		else:
			file = sys.stdin
		feature = load_sample(file)
		feature_matrix = normalize_feature_matrix(feature['matrix'])
		#print feature_matrix
		save_sample(feature['target'], feature_matrix)
	except IOError, msg:
		print msg
		exit(1)

if __name__ == '__main__':
	main()
