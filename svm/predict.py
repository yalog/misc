#!/usr/bin/env python
'''
we use the program to train scaled sample data
'''
import sys
from svm import SVM
from texttable import Texttable

def print_class(c):
	blank = []
	for i in range(10):
		blank.append('   ')
	table = Texttable()
	table.set_deco(Texttable.HEADER)
	for cs,item in c.items():
		table.header(blank)
		print "Class identifier: %g"%(cs)
		row = []
		for i in item:
			row.append(i)
			if len(row) == 10:
				table.add_row(row)
				row = []
		if len(row) != 0 and len(row) < 10:
			row += blank[(len(row)):]
			table.add_row(row)
		print table.draw()
		table.reset()

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
			classcified = {}
			for index, target in target.items():
				if target not in classcified:
					classcified[target] = []
				classcified[target].append(index+1)
			'''
			for t,i in classcified.items():
				print "class %g: "%(t),
				for j in i:
					print "%g, "%(j),
				print ''
			'''
			print_class(classcified)

		except IOError, msg:
			print msg
			exit(1)

if __name__ == '__main__':
	main()
