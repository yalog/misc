#!/usr/bin/env python
'''
we use the program to train scaled sample data
'''
import sys
from svm import SVM

def usage():
	print '''
usage: ./predict.py model_file [-k] test_data_file
-k :show that the test data own accuracy classify sign
example:
	./predict.py train.model -k test.sacle.data
	'''

def main():
	if len(sys.argv) < 3:
		usage()
		exit(1)
	else:
		model_file = sys.argv[1]
		if len(sys.argv) == 3:
			is_known = False
			test_file = sys.argv[2]
		else:
			test_file = sys.argv[3]
			is_known = True

		try:
			svm = SVM(test_file)
			svm.load_model(model_file)
			if is_known:
				ret = svm.predict_known()
				target = ret['target']
				print "Accuracy Rate:%.2f%%"%(ret['acc'] * 100)
			else:
				target = svm.predict()
			print 'Classified Result:'
			print target
		except IOError, msg:
			print msg
			exit(1)

if __name__ == '__main__':
	main()
