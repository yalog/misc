#!/usr/bin/env python
'''
we use the program to train scaled sample data
'''
import sys, getopt
from svm import SVM

def usage(msg = None):
	if msg != None:
		print msg
		print 'Try `./train.py -h` for more'
	else:
		print '''
usage: ./train.py [options] scale_data_file
options:
-h print help info,just this
-c set the cost value for SVM(default is 5)
-g set the gamma value for kernel(default is 1)

example:
	./train.py -c 5 -g 1 scale_tain.data
	'''

def main():
	param = {}
	param['cost'] = 5
	param['gamma'] = 1

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hc:g:')
	except getopt.GetoptError, msg:
		usage(msg)
		exit(1)
	
	for opt, val in opts:
		if opt == '-h':
			usage()
			exit()
		elif opt == '-c':
			param['cost'] = float(val)
		elif opt == '-g':
			param['gamma'] = float(val)
	
	if len(args) != 1:
		usage('Must specify scaled train data file')
		exit(1)

	try:
		svm = SVM(args[0])
		svm.train(param['cost'], param['gamma'])
		svm.save_model()
	except IOError, msg:
		print msg
		exit(1)

if __name__ == '__main__':
	main()
