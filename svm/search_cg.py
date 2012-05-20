#!/usr/bin/env python
import sys

#return C,g grid data
def init_cg():
	grid = {}
	#can set parameters from argment
	c_min, c_step, c_max = -5, 1, 5
	g_min, g_step, g_max = -5, 1, 5

	grid['c'] = []
	for c in range(c_min, c_max, c_step):
		grid['c'] += [2 ** c]
	
	grid['g'] = []
	for g in range(g_min, g_max, g_step):
		grid['g'] += [2 ** c]

	return grid

#when the data is very large,load feature vector by requitment
def load_train_set(scale_train_file):
	feature_matrix = []
	feature_vector = []

	for line in open(scale_train_file):
		fields = line.split()
		fea

	return []

#use multi thread to quicken calculate
def search(scale_train_data, cg_grid):
	return {'c':0, 'g':0}

class worker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.work_queue = Queue()
		self.result_queue = Queue()

	def add_work(self, work_item):
		return self.work_queue.put(work_item)
	
	def get_result(self):
		return self.result_queue.get()

	def run(self):
		self.calculate_SVM()

	def calculate_SVM(self):
		#call svm module
		return 

def exit_with_help():
	print """
usage:./find_cg.py scale_train_file
	"""
	exit(1)

def main():
	if len(sys.argv) < 2:
		exit_with_help()

	scale_train_data = load_train_set(sys.argv[1])
	cg_grid = init_cg()

	cg = cv_find(scale_train_data, cg_grid)
	for key,value in cg.items():
		print "%s:%d"%(key, value)

main()
