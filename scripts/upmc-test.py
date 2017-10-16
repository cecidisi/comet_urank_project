import multiprocessing as mp
import time


def dosomething(item):
	item['elem'] += 1
	return item


def run():
	cores = int(mp.cpu_count() * .75)
	print cores

	arr = []
	for i in range(100000):
		arr.append({ 'elem': i })

	print len(arr)

	tmsp = time.time()
	pool = mp.Pool(processes = cores)
	pool.map(dosomething, arr)
	jobs = pool.map(dosomething, arr)
	pool.close()
	pool.join()

	tmsp = time.time() - tmsp
	print 'Time = ' + str(tmsp)
	# print jobs


# if __name__ == "__main__":
# 	run()
