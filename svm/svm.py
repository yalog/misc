#!/usr/bin/env python
import sys

'''
This is a interface for both CLI and python module.
At this version,we use whole vector matrix,but thin vector matrix
'''

#The interface for python
#train
def svm_train():

def svm_predict():

def load_svm_model():

def save_svm_model():

####

#The interface for CLI
#We package the python module interface into CLI by explaining command argment

def exit_with_help():
	print '''
usage:./svm [option] file_train
	'''
	exit(1)

def main():
	param = {}
	#set default settings
	param['cmd'] = 'train'
	param['train_file'] = ''
	param['predict_file'] = ''
	param['predict_accuracy'] = False #wheather calculter predict accucy
	param['c'] = 5
	param['g'] = 5
	
	i  = 1
	while i < len(sys.argv):
		if sys.argv[i] == '-t':
			i += 1
			param['cmd'] = 'train'
		elif sys.argv[i] == '-p':
			i += 1
			param['cmd'] = 'predict'
		elif sys.argv[i] == '-a':
			i += 1
			param['predict_accuy'] = True

if __name == '__main__':
	main()
