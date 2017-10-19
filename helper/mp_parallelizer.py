import multiprocessing as mp
from django import db

class Parallelizer:

	@classmethod
	def run(cls, func, iterable, processes=0, async=True, db_close=False):
		if db_close:
			db.connections.close_all()
		if not processes:
			processes = max(10, int(mp.cpu_count() * .75))

		pool = mp.Pool(processes=processes)
		jobs = None
		if async:
			jobs = pool.map_async(func, iterable)
			jobs = jobs.get()
		else:
			jobs = pool.map(func, iterable)
		pool.close()
		pool.join()

		return jobs