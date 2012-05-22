import math
import random
#define kernal funciton
class Kernel:
	def __init__(self, k_type, g):
		self.__gamma = None#The gamma paramter in kernel function
		self.__kernel_function = None #kernel function ponitor

		if k_type == 'rbf':
			self.__kernel_function = self.__kernel_rbf
		elif k_type == 'linear':
			self.__kernel_function = self.__kernel_linear
		else:
			raise Exception, 'specified kernel type error'

		self.__gamma = g
	
	#This is a public interface for calculate kernel function value
	def fun(self, x1, x2):
		return self.__kernel_function(x1, x2)
	
	#calculate dot product value between vector x1 and x2
	def __dot(self, x1, x2):
		sum = 0

		for i,value in enumerate(x1):
			sum += x1[i] * x2[i]

		return sum
			

	def __kernel_rbf(self, x1, x2):
		#we can cache dot(xi,xi)
		return math.exp(-self.__gamma * 
				(self.__dot(x1, x1) + self.__dot(x2, x2) - 2 * self.__dot(x1, x2)))

	def __kernel_linear(self, x1, x2):
		sum = 0
		
		for i, value in enumerate(x1):
			sum += x1[i] * x2[i]
		return sum
########## end of kernel

#def calculate_obj():

'''
smo algorithm is packaged into a class.
The main algorithm is realized by the fake code in Platt`s paper.
In the algorithm,we don`t handle the condition where training points is unbalance.
'''
class SMO:
	__y = [] #target set
	__x = [] #train point set
	__b = 0  #the threshold b of the SVM
	__alpha = []
	__l = 0 #the train point length
	__c = 0
	__g = 0 #gamma
	__kernel = [] #store the value of kernal
	__E = {} #store the value of error
	__active_set = [] #contain the alpha index that is bounded
	__eps = 10 ** -3
	__tol = 0.01

	def __init__(self, y, x, l, c = 5, g = 5, k_type = 'rbf'):
		self.__y = y
		self.__x = x
		self.__l = l
		self.__c = c
		self.__g = g
		
		#initialize alpha array
		for i in range(l):
			self.__alpha.append(0)

		#initialize kernel matrix
		self.__init_kernel(k_type)

		#initialize error array
		for i in range(l):
			self.update_error(i)
		
	def __init_kernel(self, k_type):
		kernel = Kernel(k_type, self.__c)

		for i in range(self.__l):
			self.__kernel.append([])

			for j in range(self.__l):
				self.__kernel[i].append(kernel.fun(self.__x[i], self.__x[j]))
	

	def solve(self):
		num_changed = 0
		examine_all = 1
		max_iter = 100000
		iter = 0
		#find the first alpha in outter cycle
		while iter < max_iter and (num_changed > 0 or examine_all):
			iter += 1
			num_changed = 0
			if examine_all:
				for i in range(self.__l):
					num_changed += self.examine_example(i)
			else:
				for i in self.__active_set:
					num_changed += self.examine_example(i)

			if examine_all == 1:
				examine_all = 0
			elif num_changed == 0:
				examine_all = 1

		if iter >= max_iter:
			 raise Exception, 'out of max iteration times'
		
		#return bounded alpha value
		alpha = []
		for i, v in enumerate(self.__alpha):
			if v > 0 and v < self.__c:
				alpha.append((i, v))

		return (alpha, self.__b)

	#the inner cycle where find the second alpha
	def examine_example(self, i2):
		y2 = self.__y[i2]
		r2 = self.__E[i2] * y2

		if self.un_kkt(i2):
			if len(self.__active_set) > 1:
				i1 = self.search_max_error(i2)
				if self.take_step(i1, i2):
					return 1

			random.shuffle(self.__active_set)
			for i in self.__active_set:
				if self.take_step(i, i2):
					return 1

			all = range(self.__l)
			random.shuffle(all)
			for i in all:
				if self.take_step(i, i2):
					return 1

		return 0

	def search_max_error(self, i2):
		max_i = -1
		max_diff = 0

		for i in range(self.__l):
			if abs(self.__E[i] - self.__E[i2]) > max_diff:
				max_diff = abs(self.__E[i] - self.__E[i2])
				max_i = i
		
		return max_i

	#the algorithm that calculate optimization value between two alpha
	def take_step(self, i1, i2):
		if i1 == i2:
			return False

		s = self.__y[i1] * self.__y[i2]
		if s == -1:
			L = max(0, self.__alpha[i2] - self.__alpha[i1])
			H = min(self.__c, self.__c + self.__alpha[i2] - self.__alpha[i1])
		else:
			L = max(0, self.__alpha[i2] + self.__alpha[i1] - self.__c)
			H = min(self.__c, self.__alpha[i2] + self.__alpha[i1])

		if L == H:
			return False

		k11 = self.__kernel[i1][i1]
		k12 = self.__kernel[i1][i2]
		k22 = self.__kernel[i2][i2]
		eta =  2 * k12 - k11 - k22

		#usually,the eta is less than 0
		if eta < 0:
			a2 = self.__alpha[i2] - self.__y[i2] * (self.__E[i1] - self.__E[i2]) / eta
			if a2 < L:
				a2 = L
			elif a2 > H:
				a2 = H
		else:#handle the unusual circumstances
			#all of the code beblow are realization of formula in papers
			f1 = self.__y[i1] * self.__E[i1] - self.__alpha[i1] * self.__kernel[i1][i1] - s * self.__alpha[i2] * self.__kernel[i1][i2]
			f2 = self.__y[i2] * self.__E[i2] - self.__alpha[i2] * self.__kernel[i2][i2] - s * self.__alpha[i1] * self.__kernel[i1][i2]
			L1 = self.__alpha[i1] + s * (self.__alpha[i2] - L)
			H1 = self.__alpha[i1] + s * (self.__alpha[i2] - H)
			
			Lobj = L1 * f1 + L * f2 + 0.5 * L1 * L1 * self.__kernel[i1][i1] + 0.5 * L * L * self.__kernel[i2][i2] + s * L * L1 * self.__kernel[i1][i2]
			Hobj = H1 * f1 + H * f2 + 0.5 * L1 * L1 * self.__kernel[i1][i1] + 0.5 * H * H * self.__kernel[i2][i2] + s * H * H1 * self.__kernel[i1][i2]

			if Lobj < Hobj - self.__eps:
				a2 = L
			elif Lobj > Hobj + self.__eps:
				a2 = H
			else:
				a2 = self.__alpha[i2]

		#if a2 has not enough increase
		if abs(a2 - self.__alpha[i2]) < self.__eps * (a2 + self.__alpha[i2]+ self.__eps):
			return False

		a1 = self.__alpha[i1] + s * (self.__alpha[i2] - a2)

		#add selected alpha into active set (0 < alpha < C)
		if a1 > 0 and a1 < self.__c:
			if i1 not in self.__active_set:
				self.__active_set.append(i1)
		elif i1 in self.__active_set:
			self.__active_set.remove(i1)
		
		if a2 > 0 and a2 < self.__c:
			if i2 not in self.__active_set:
				self.__active_set.append(i2)
		elif i2 in self.__active_set:
			self.__active_set.remove(i2)

		#update threshold b
		b1 = self.__b - self.__E[i1] - \
			 self.__y[i1] * (a1 - self.__alpha[i1]) * self.__kernel[i1][i1] - \
			 self.__y[i2] * (a2 - self.__alpha[i2]) * self.__kernel[i2][i1]
		b2 = self.__b - self.__E[i2] - \
			 self.__y[i1] * (a1 - self.__alpha[i1]) * self.__kernel[i1][i2] - \
			 self.__y[i2] * (a2 - self.__alpha[i2]) * self.__kernel[i2][i2]
		if a1 > 0 and a1 < self.__c:
			self.__b = b1
		elif a2 > 0 and a2 < self.__c:
			self.__b = b2
		else:
			self.__b = (b1 + b2) / 2
	
		#update alpha
		self.__alpha[i1] = a1
		self.__alpha[i2] = a2
		#try to find wheather need to write to active set

		#update error to cache
		self.update_error(i1)
		self.update_error(i2)

		return True


	def update_error(self, i_u):
		sum = 0

		for i in range(self.__l):
			sum += self.__alpha[i] * self.__y[i] * self.__kernel[i][i_u]

		self.__E[i_u] = sum - self.__y[i_u] + self.__b
	
	def un_kkt(self, i):
		ri = self.__E[i] * self.__y[i]
	
		#subject KKT condition under centain precision
		if (ri < -self.__tol and self.__alpha[i] < self.__c) or\
			(ri > self.__tol and self.__alpha[i] > 0):
			return True
		else:
			return False
################# end of SMO
