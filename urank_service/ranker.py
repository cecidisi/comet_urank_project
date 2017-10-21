import copy
from helper.bcolors import *
from .rs_content_based import *
from .rs_collaborative_filtering import *
from helper.mp_parallelizer import *
from functools import partial
import time
import multiprocessing as mp
from helper.pretty_time import *

def update_worker(recommender, conf_rs, features, d):
	idx = d['idx']
	doc_id = d['id']
	d['ranking']['prev_pos'] = d['ranking']['pos']
	d['ranking']['overall'] = { 'score': 0.0 }

	for rs in conf_rs:
		rs_name = rs['name']
		if rs['active']:
			# CHECK HERE!!!!!!
			rs_resp = recommender[rs_name].get_score(idx, doc_id, features, rs)
			d['ranking'][rs_name] = {
				'score' : rs_resp['score'],
				'details' : rs_resp['details']
			}
	return d


def normalization_worker(recommender, rs_conf, d):
	for conf in rs_conf:
		if conf['active']:
			rs_name = conf['name']
			max_score = recommender[rs_name].get_max_score()
			val_before = d['ranking'][rs_name]['score']
			d['ranking'][rs_name]['score'] = 0.0
			if max_score:
				d['ranking'][rs_name]['score'] = \
					(float(d['ranking'][rs_name]['score']) / max_score) * float(conf['weight'])
			for detail in d['ranking'][rs_name]['details']:
				detail['score'] = 0.0
				if max_score:
					detail['score'] = (float(detail['score']) / max_score) * float(conf['weight'])
			d['ranking']['overall']['score'] += d['ranking'][rs_name]['score']
	return d


class Ranker:

	rs = {
		'CB': RSContentBased(),
		'CF': RSCollaborativeFiltering()
	}
	# cores = max(10, mp.cpu_count()*.75)
	# pool = mp.Pool(processes=3)

	def __init__(self):
		self.clear()
		


	@staticmethod
	def assign_positions(ranking, rank_by):
		cur_score = float('inf')
		cur_pos = 1
		items_in_cur_pos = 0
		for d in ranking:
			if d['ranking'][rank_by]['score']:
				if d['ranking'][rank_by]['score'] < cur_score:
					# print d['ranking'][rank_by]['score']
					cur_pos = cur_pos + items_in_cur_pos
					cur_score = d['ranking'][rank_by]['score']
					items_in_cur_pos = 1
				else:
					items_in_cur_pos +=1
				d['ranking']['pos'] = cur_pos
			else:
				d['ranking']['pos'] = 0
			# compute shift
			d['ranking']['pos_changed'] = d['ranking']['prev_pos'] - d['ranking']['pos'] if d['ranking']['prev_pos'] else 1000
		return ranking



	def set_data(self, data):
		self.data = data[:]
		for idx, d in enumerate(self.data): 
			d['idx'] = idx
			d['ranking'] = {
				'pos': 0,
				'pos_changed': 0,
				'prev_pos': 0
			}
		self.ranking = self.data[:]


	#  For CB
	def load_doc_keywords(self, doc_keywords):
		Ranker.rs['CB'].set_doc_keywords(doc_keywords)


	#  For CF
	def load_neighbors(self, _neighbors, sim_ui):
		active_neighbors = self.load_sim_item_user(sim_ui)
		active_neighbors.keys()
		filtered_neighbors = []
		for n in _neighbors:
			vid = n['neighbor']['id']
			if vid in active_neighbors:
				self.neighbors[vid] = n['score']
				filtered_neighbors.append(n)
		Ranker.rs['CF'].set_sim_v(self.neighbors)
		return filtered_neighbors


	#  For CF
	def load_sim_item_user(self, sim_ui):
		# print sim_ui
		active_neighbors = {}
		sim_item_user = {}
		for s in sim_ui:
			vid = s['user_id']
			pid = s['talk_id']
			# add item entry
			if pid not in sim_item_user:
				sim_item_user[pid] = {}	
			# assign sim value to pid -> vid entry
			sim_item_user[pid][vid] = s['score']

			if vid not in active_neighbors:
				active_neighbors[vid] = 0
			active_neighbors[vid] +=1

		Ranker.rs['CF'].set_sim_iv(sim_item_user)
		return active_neighbors

		# idx = 0
		# for vid, count in active_neighbors.iteritems():
		# 	idx+= 1
		# 	print '#'+str(idx) + '. vid ' + str(vid) + ' --> ' + str(count)
		

	@staticmethod
	def compute_score(d, features, rs_conf):
		idx = d['idx']
		doc_id = d['id']
		d['ranking']['prev_pos'] = d['ranking']['pos']
		d['ranking']['overall'] = { 'score': 0.0 }

		for conf in rs_conf:
			RS = conf['name']
			if conf['active']:
				rs_resp = Ranker.rs[RS].get_score(idx, doc_id, features, conf)
				d['ranking'][RS] = {
					'score' : rs_resp['score'],
					'details' : rs_resp['details']
				}
		return d


	@staticmethod
	def normalize(x, max_x):
		value = float(x) / float(max_x) if max_x else 0.0
		if max_x:
			return float(x) / float(max_x)
		return 0.0


	@staticmethod
	def normalize_score(d, rs_conf):
		for conf in rs_conf:
			if conf['active']:
				RS = conf['name']
				max_score = Ranker.rs[RS].get_max_score()
				val_before = d['ranking'][RS]['score']
				d['ranking'][RS]['score'] = Ranker.normalize(d['ranking'][RS]['score'], max_score) * float(conf['weight'])
				# check if it works!!!!!
				for detail in d['ranking'][RS]['details']:
					detail['score'] = Ranker.normalize(detail['score'], max_score) * float(conf['weight'])
				d['ranking']['overall']['score'] += d['ranking'][RS]['score']
		return d
		



	# ,query, utags
	def update(self, conf, features):
		print_blue('================= FEATURES ======================')
		print features
		print_blue('================== RS CONF ======================')
		print conf['rs']
		
		self.ranking = self.ranking[:]
		
		print 'Empty features = ' + str(Ranker.are_features_empty(features))
		if Ranker.are_features_empty(features):
			print_blue('Returning here')
			# return self.reset()

		#  Compute recommendation scores		
			
		tmsp = time.time()

		## Update scores
		# Parallel update
		# if len(self.ranking) >= 100:
		# 	print_blue('Updating with multiprocessing ...')

		# 	worker_upd = partial(update_worker, Ranker.rs, conf['rs'], features)
		# 	# job = Ranker.pool.map_async(worker, self.ranking)
		# 	try:
		# 		# self.ranking = Parallelizer.run(worker_upd, self.ranking)
		# 		print 'Start mp update'
		# 		pool = mp.Pool()
		# 		self.ranking = pool.map(worker_upd, self.ranking[:1000])
		# 		pool.close()
		# 		pool.join()
		# 	except Exception, e:
		# 		print 'ERROR updating scores'
		# 		print e
		# 		print 'Running serial update instead'
		# 		self.ranking = [Ranker.compute_score(d, features, conf['rs']) for d in self.ranking] 
		# 	print_green('Update time = ' + str(time.time() - tmsp))

		# 	worker_norm = partial(normalization_worker, Ranker.rs, conf['rs'])
		# 	try:
		# 		# self.ranking = Parallelizer.run(worker_norm, self.ranking)
		# 		print 'Start mp normalize'
		# 		pool = mp.Pool()
		# 		self.ranking = pool.map(worker_upd, self.ranking)
		# 		pool.close()
		# 		pool.join()
		# 	except Exception, e:
		# 		print 'ERROR normalizing scores'
		# 		print e
		# 		print 'Running serial normalization instead'
		# 		self.ranking = [Ranker.normalize_score(d, conf['rs']) for d in self.ranking]
		# 		print_green('Update + Normalization = ' + str(time.time() - tmsp))
		# else:
		print_blue('Serial Update')
		self.ranking = [Ranker.compute_score(d, features, conf['rs']) for d in self.ranking] 
		print_green('Update time = ' + str(time.time() - tmsp))
		# Normalize
		self.ranking = [Ranker.normalize_score(d, conf['rs']) for d in self.ranking]
		print_green('Update + Normalization time = ' + str(time.time() - tmsp))
		# Sort and assign positions
		rank_by = conf['rankBy']
		self.ranking = sorted(self.ranking, key=lambda d: d['ranking'][rank_by]['score'], reverse=True)
		self.ranking = Ranker.assign_positions(self.ranking, rank_by)
		print_green('Update + normalization + sorting time = ' + str(time.time() - tmsp))

		return self.get_ranking()



	@staticmethod 
	def are_features_empty(features):
		for fvalues in features.values():
			if len(fvalues):
				return False
		return True



	def get_ranking(self, offset=0, limit=50):
		limit = offset + limit
		# Return a copy by value
		# return copy.deepcopy(self.ranking[offset:100]) 
		print "Ranker: returned " + str(len(self.ranking))
		return copy.deepcopy(self.ranking[:]) 


	def get_item(self, idx):
		return copy.deepcopy(self.ranking[idx])


	def reset(self):
		self.ranking = self.data[:]
		return self.ranking
		

	def clear(self):
		self.data = []
		# self.doc_keywords = []
		self.ranking = []
		self.query = []
		self.neighbors = {}
		return self.ranking

