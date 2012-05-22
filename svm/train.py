#!/usr/bin/env python
'''
we use the program to train scaled sample data
'''
import sys
from svm import SVM

def usage():
	print '''
usage: ./train.py scale_data_file
example:
	./train.py train.sacle.data
	'''

def main():
	if len(sys.argv) < 2:
		usage()
		exit(1)
	else:
		try:
			svm = SVM(sys.argv[1])
			svm.train()
			svm.save_model()
		except IOError, msg:
			print msg
			exit(1)

if __name__ == '__main__':
	main()
