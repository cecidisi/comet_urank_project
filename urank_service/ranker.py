import copy
from helper.bcolors import *
from .rs_content_based import *
from .rs_collaborative_filtering import *
from helper.mp_parallelizer import *
from functools import partial
import time
import multiprocessing as mp
from helper.pretty_time import *



class Ranker:

	rs = {
		'CB': RSContentBased(),
		'CF': RSCollaborativeFiltering()
	}
	# cores = max(10, mp.cpu_count()*.75)
	# pool = mp.Pool(processes=3)

	def __init__(self):
		self.ranking = []
		self.prev_pos_mapping = {}
		self.query = []
		self.neighbors = {}
		self.rank_by = ''
		


	@staticmethod
	def assign_positions(ranking, rank_by, prev_pos_mapping):
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
			prev_pos = prev_pos_mapping[d['id']] if d['id'] in prev_pos_mapping else 0
			d['ranking']['prev_pos'] = prev_pos
			d['ranking']['pos_changed'] = prev_pos - d['ranking']['pos'] if prev_pos > 0 else 1000
		return ranking



	def set_data(self, data):
		if len(self.ranking):
			self.prev_pos_mapping = { d['id']: d['ranking']['pos'] for d in self.ranking }
		self.ranking = data[:]
		for idx, d in enumerate(self.ranking): 
			d['idx'] = idx
			d['ranking'] = {
				'pos': 0,
				'pos_changed': 0,
				'prev_pos': 0
			}


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

		for rs_name in Ranker.rs.keys():
			Ranker.rs[rs_name].clear()
		
		# print 'Empty features = ' + str(Ranker.are_features_empty(features))
		# if Ranker.are_features_empty(features):
		# 	print_blue('Returning here')
		# 	# return self.reset()

		#  Compute scores		
		tmsp = time.time()
		self.ranking = [Ranker.compute_score(d, features, conf['rs']) for d in self.ranking] 
		print_green('Update time = ' + str(time.time() - tmsp))
		# Normalize
		self.ranking = [Ranker.normalize_score(d, conf['rs']) for d in self.ranking]
		print_green('Update + Normalization time = ' + str(time.time() - tmsp))
		# Sort and assign positions
		self.rank_by = conf['rankBy']
		self.ranking = sorted(self.ranking, key=lambda d: d['ranking'][self.rank_by]['score'], reverse=True)
		self.ranking = Ranker.assign_positions(self.ranking, self.rank_by, self.prev_pos_mapping)
		print_green('Update + normalization + sorting time = ' + str(time.time() - tmsp))
		print self.ranking[0]
		return self.get_ranking()



	def filter_by_year(self, from_year, to_year):
		filtered_ranking = [d for d in self.ranking \
			if d['year'] >= from_year 
			and d['year'] <= to_year ]
		self.set_data(filtered_ranking)
		self.ranking = Ranker.assign_positions(self.ranking, self.rank_by, self.prev_pos_mapping)
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
		print "Ranker: returned " + str(len(self.ranking))
		return copy.deepcopy(self.ranking[:]) 
		# return self.ranking[:]


	def get_item(self, idx):
		return copy.deepcopy(self.ranking[idx])


	def reset(self):
		self.ranking = self.data[:]
		return self.ranking
		

	def clear(self):
		self.ranking = []
		self.prev_pos_mapping = {}
		self.query = []
		self.neighbors = {}
		return self.ranking

