#!/usr/bin/env python
import sys

#import train algorithm
from smo import SMO
from smo import Kernel

'''
This is a interface for both CLI and python module.
At this version,we use whole vector matrix,but thin vector matrix.
And the version just realized binary classify
'''

#The interface for python
class SVM:
	#if want to train svm model,the sample target value must be accuracy specified
	#we don`t assume anyothers values 
	def __init__(self, sample_file):
		self.__model = None #svm model
		self.__x = [] #train points matrix
		self.__y = []#train points target value array

		self.load_sample(sample_file)

	#call corresponding algorithm to train,and return svm model
	def train(self, cost = 5, gamma = 0.5, kernel_type = 'rbf'):
		smo = SMO(self.__y, self.__x, len(self.__y), cost, gamma, kernel_type)
		resolve = smo.solve()
		
		model  = {}
		model['kernel_type'] = kernel_type
		model['gamma'] = gamma
		model['cost'] = cost
		model['rho'] = resolve[1]
		model['sv'] = {}
		for i, v in resolve[0]:
			model['sv'][i] = {}
			model['sv'][i]['ya'] = self.__y[i] * v
			model['sv'][i]['vector'] = self.__x[i]

		self.__model = model

	#predict target value which input points corresponding
	def predict(self):
		self.__model = model
		target = {}

		for i, v in enumerate(self.__x):
			target[i] = self.decision(v)
		
		return target
	
	#when model is setted, using the model to decision
	def decision(self, sample_vector):
		if self.__model == None:
			raise Exception, 'need to load or train model before decision'

		sum = 0
		#need to opimize
		kernel = Kernel(self.__model['kernel_type'], self.__model['gamma'])

		for i, sv in self.__model['sv'].items():
			sum += sv['ya'] * kernel.fun(sv['vector'], sample_vector)

		if sum + self.__model['rho'] < 0:
			return -1
		elif sum + self.__model['rho'] > 0:
			return 1
		else:
			return 0

	#load svm model file to memory
	def load_model(self, model_file):
		lines = open(model_file).readlines()
		if len(lines) < 7:
			raise Exception, 'SVM model file format error'
		
		#过滤注释，还是要for
		self.__model = {}
		s = lines[0].strip().strip("\n").split(':')
		self.__model['kernel_type'] = s[1]
		s = lines[1].trip().strip("\n").plit(':')
		self.__model['gamma'] = float(s[1])
		s = lines[2].strip().strip("\n").split(':')
		self.__model['rho'] = float(s[1])
		s = lines[3].strip().strip("\n").split(':')
		self.__model['cost'] = float(s[1])
		
		self.__model = []
		for line in self.__model[4:]:
			if line.startswith('#'):
				continue

			line = line.strip()
			line = line.strip("\n") #may can not work in across defferent OS
			fields = line.split(' ')#in default,space is used to split
			point = {}
			point['ya']int(fields.pop(0))
			fields = map(lambda x:float(x), fields)
			point['vector'] = fields
			self.__model.append(ponit)

	#if model_file is None ,return string content of model file,otherwise wirte to file
	def save_model(self, is_ret = False):
		if self.__model == None:
			raise Exception, 'must training before'

		if is_ret:
			return self.__model
		else:
			#output head
			print '#This is file of SVM model from sample training'
			print "kernel_type:%s"%(self._model['kernel_type'])
			print "gamma:%s"%(self._model['gamma'])
			print "rho:%s"%(self._model['rho'])
			print "cost:%s"%(self._model['cost'])
			#output body
			print '' #print spliting line
			str = ''
			for i in self.__model['sv']:
				str = "%d"%(i['ya'])
				for v in i['vector']:
					str += " %g"%(v)
				print str


	#laod self defined train data format
	def load_sample(self, sample_file):
		for line in open(sample_file):
			if line.startswith('#'):
				continue

			line = line.strip()
			line = line.strip("\n") #may can not work in across defferent OS
			fields = line.split(' ')#in default,space is used to split
			self.__y.append(int(fields.pop(0)))
			fields = map(lambda x:float(x), fields)
			self.__x.append(fields)

	def cross_validate(k = 2):
		return True

####

#The interface for CLI
#We package the python module interface into CLI by explaining command argment

def exit_with_help():
	print '''
usage:./svm train|predict []file
options:
-t 
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
			param['predict_accuracy'] = True
	
	svm = SVM('DNA.train')
	svm.train()
	model  = svm.save_model()
	svm = SVM('DNA.test')
	print svm.predict(model)

if __name__ == '__main__':
	main()
