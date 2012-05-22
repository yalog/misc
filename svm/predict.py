#!/usr/bin/env python
'''
we use the program to train scaled sample data
'''
import sys
from svm import SVM

def usage():
	print '''
usage: ./predict.py model_file test_data_file
example:
	./predict.py train.model test.sacle.data
	'''

def main():
	if len(sys.argv) < 3:
		usage()
		exit(1)
	else:
		try:
			svm = SVM(sys.argv[2])
			svm.load_model(sys.argv[1])
			svm.predict()
		except Exception, msg:
			print msg
			exit(1)

if __name__ == '__main__':
	main()
