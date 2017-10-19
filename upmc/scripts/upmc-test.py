# import multiprocessing as mp
import time
from helper.mp_parallelizer import *


def dosomething(item):
	i1, i2 = item
	print item
	return item


def run():
	cores = int(mp.cpu_count() * .75)
	print cores
	arr = []
	for i in range(20):
		arr.append((i, i+1))

	dic = {}
	for i in range(20):
		dic[i] = i+1


	tmsp = time.time()
	# pool = mp.Pool(processes = cores)
	# # jobs = pool.map_async(dosomething, arr)
	# jobs = pool.map_async(dosomething, dic.iteritems())
	# pool.close()
	# pool.join()
	# print jobs.get()
	jobs = Parallelizer.run(dosomething, dic.iteritems())
	tmsp = time.time() - tmsp
	print 'Time = ' + str(tmsp)
	# print jobs


# if __name__ == "__main__":
# 	run()
