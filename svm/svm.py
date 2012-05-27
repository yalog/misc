#!/usr/bin/env python
import sys

#import train algorithm
from smo import SMO
from smo import Kernel

'''
This is a interface for python module.
At this version,we use whole vector matrix,but thin vector matrix.
And the version just realized binary classify

Code Tree:
	Class SVM:
	-funtions
		train(self, cost = 5, gamma = 0.5, kernel_type = 'rbf')
		predict(self)
		predict_known(self)
		decision(self, sample_vector)
		load_model(self, model_file)
		save_model(self, is_ret = False)
		load_sample(self, sample_file)
		cross_validate(self, cost, gamma, k = 2, kernel_type = 'rbf')
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
		
		model = {}
		model['kernel_type'] = kernel_type
		model['gamma'] = gamma
		model['cost'] = cost
		model['rho'] = resolve[1]
		model['sv'] = []
		for i, v in resolve[0]:
			point = {}
			point['ya'] = self.__y[i] * v
			point['vector'] = self.__x[i]
			model['sv'].append(point)

		self.__model = model

	#predict target value which input points corresponding
	def predict(self):
		target = {}

		for i, v in enumerate(self.__x):
			target[i] = self.decision(v)
		
		return target
	
	#append accuracy rate
	def predict_known(self):
		target = self.predict()
		acc_num = 0.0
		
		for i, indent in enumerate(self.__y):
			if indent == target[i]:
				acc_num += 1

		return {'acc':acc_num/len(target), 'target':target}
	
	#when model is setted, using the model to decision
	def decision(self, sample_vector):
		if self.__model == None:
			raise Exception, 'need to load or train model before decision'

		sum = 0
		#need to opimize
		kernel = Kernel(self.__model['kernel_type'], self.__model['gamma'])

		for sv in self.__model['sv']:
			sum += sv['ya'] * kernel.fun(sv['vector'], sample_vector)

		if sum + self.__model['rho'] < 0:
			return -1
		elif sum + self.__model['rho'] > 0:
			return 1
		else:
			return 0

	#load svm model file to memory
	def load_model(self, model_file):
		lines = []
		for line in open(model_file):
			if line.startswith('#'):
				continue
			line = line.strip()
			line = line.strip("\n") #may can not work in across defferent OS
			if len(line) == 0: continue
			lines.append(line)

		if len(lines) < 6:
			raise Exception, 'SVM model file format error'
		
		self.__model = {}
		for head in lines[:4]:
			s = head.split(':')
			if len(s) != 2:
				raise Exception, 'SVM model file format error'
			if s[0] == 'kernel_type':
				self.__model['kernel_type'] = s[1]
			else:
				self.__model[s[0]] = float(s[1])
		
		self.__model['sv'] = []
		for body in lines[4:]:
			fields = body.split(' ')#in default,space is used to split
			fields = map(lambda x:float(x), fields)
			point = {}
			point['ya'] = fields[0]
			point['vector'] = fields[1:]
			self.__model['sv'].append(point)

	#if model_file is None ,return string content of model file,otherwise wirte to file
	def save_model(self, is_ret = False):
		if self.__model == None:
			raise Exception, 'must training before'

		if is_ret:
			return self.__model
		else:
			#output head
			print '#This is file of SVM model from sample training'
			print "kernel_type:%s"%(self.__model['kernel_type'])
			print "gamma:%s"%(self.__model['gamma'])
			print "rho:%s"%(self.__model['rho'])
			print "cost:%s"%(self.__model['cost'])
			#output body
			print '' #print spliting line
			str = ''
			for i in self.__model['sv']:
				str = "%g"%(i['ya'])
				for v in i['vector']:
					str += " %g"%(v)
				print str


	#load self defined train data format
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

	#cross validate and return average accuracy rate
	def cross_validate(self, cost, gamma, k = 2, kernel_type = 'rbf'):
		x = self.__x
		y = self.__y
		accs = []
		valid_set = {}

		#divide train set into k group
		for i,v in enumerate(x):
			try:
				valid_set[i % k].append(i)
			except KeyError:
				valid_set[i % k] = []
				valid_set[i % k].append(i)

		for i, valid in valid_set.items():
			#train
			self.__x = []
			self.__y = []
			for i,v in enumerate(x):
				if i not in valid:
					self.__x.append(x[i])
					self.__y.append(y[i])
			self.train(cost, gamma, kernel_type)

			#predict
			self.__x = []
			self.__y = []
			for i in valid:
				self.__x.append(x[i])
				self.__y.append(y[i])
			predict = self.predict_known()
			accs.append(predict['acc'])
			
		#calculate average accuracy rate
		sum = 0.0
		for i in accs:
			sum += i
		
		self.__x = x
		self.__y = y

		return sum / len(accs)
#### end of SVM
