#!/usr/bin/env python
import sys
import threading
from Queue import Queue
from Queue import Empty
from svm import SVM

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
		grid['g'] += [2 ** g]

	return grid

#the thread which do cross validate
class Worker(threading.Thread):
	def __init__(self, train_file, work_queue, result_queue):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
		self.result_queue = result_queue
		self.train_file = train_file

	def run(self):
		while True:
			try:
				cg = self.work_queue.get_nowait()
				svm = SVM(sys.argv[1])
				avg_acc = svm.cross_validate(cg[0],cg[1])
				self.result_queue.put((cg[0], cg[1], avg_acc))
			except Empty:
				return

def usage():
	print """
usage:./search_cg.py scale_train_file
	"""

def main():
	if len(sys.argv) < 2:
		usage()
		exit(1)

	cg_grid = init_cg()

	#all of blow will cause a dead lock,when put task into queue
	#add task to worker
	work_queue = Queue()
	result_queue = Queue()
	#avg_acc = []
	for cost in cg_grid['c']:
		for g in cg_grid['g']:
			work_queue.put((cost, g))
	
	#create work thread
	worker = []
	for i in range(4):
		work = Worker(sys.argv[1], work_queue, result_queue)
		work.start()
		worker.append(work)
	#wait for worker finish
	for i in worker:
		i.join()

	#get result
	avg_acc = []
	while True:
		try:
			avg_acc.append(result_queue.get(False))
		except Empty:
			break
	#get the most optimization cost and gamma
	op_c = avg_acc[0][0]
	op_g = avg_acc[0][1]
	max_acc = avg_acc[0][2]
	for i in avg_acc:
		if i[2] < max_acc:
			continue
		elif i[2] == max_acc and i[0] >= op_c:
			continue
		op_c = i[0]
		op_g = i[1]
		max_acc = i[2]

	print "cost:%g gamma:%g acc:%g"%(op_c, op_g, max_acc)
			

if __name__ == '__main__':
	main()
