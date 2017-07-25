from conf_navigator.classes.rs_content_based import *
from conf_navigator.classes.rs_collaborative_filtering import *
from conf_navigator.classes.bcolors import *
import copy

class Ranker:

	def __init__(self):
		self.clear()
		self.rs = {
			'CB': RSContentBased(),
			'CF': RSCollaborativeFiltering()
		}


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
		self.rs['CB'].set_doc_keywords(doc_keywords)


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
		self.rs['CF'].set_sim_v(self.neighbors)
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

		self.rs['CF'].set_sim_iv(sim_item_user)
		return active_neighbors

		# idx = 0
		# for vid, count in active_neighbors.iteritems():
		# 	idx+= 1
		# 	print '#'+str(idx) + '. vid ' + str(vid) + ' --> ' + str(count)
		


	# ,query, utags
	def update(self, conf, features):
		print '================= FEATURES ======================'
		print features
		print '================== RS CONF ======================'
		print conf

		self.ranking = self.ranking[:]
		conf_map = {}
		for RS in self.rs:
			self.rs[RS].clear()
			rs_idx = next(idx for (idx, c) in enumerate(conf['rs']) if c["name"] == RS)
			conf_map[RS] = conf['rs'][rs_idx]
		
		print 'Empty features = ' + str(Ranker.are_features_empty(features))
		if Ranker.are_features_empty(features):
			print_blue('Returning here')
			# return self.reset()
		#  Compute recommendation scores
		for d in self.ranking:
			idx = d['idx']
			doc_id = d['id']
			d['ranking']['prev_pos'] = d['ranking']['pos']
			d['ranking']['overall'] = { 'score': 0.0 }

			for rs in conf['rs']:
				RS = rs['name']
				if rs['active']:
					rs_resp = self.rs[RS].get_score(idx, doc_id, features, conf_map[RS])
					d['ranking'][RS] = {
						'score' : rs_resp['score'],
						'details' : rs_resp['details']
					}
					# d['ranking']['overall']['score'] += d['ranking'][RS]['score']
		# Normalize
		for idx, d in enumerate(self.ranking):
			for rs in conf['rs']:
				if rs['active']:
					RS = rs['name']
					max_score = self.rs[RS].get_max_score()
					val_before = d['ranking'][RS]['score']
					d['ranking'][RS]['score'] = Ranker.normalize_score(d['ranking'][RS]['score'], max_score) * float(rs['weight'])
					# check if it works!!!!!
					for detail in d['ranking'][RS]['details']:
						detail['score'] = Ranker.normalize_score(detail['score'], max_score) * float(rs['weight'])
					d['ranking']['overall']['score'] += d['ranking'][RS]['score']
					# if idx ==0:
					# 	print RS  + ' weight = '+ str(rs['weight']) + ', max score = ' + str(max_score)
					# 	print d['ranking']
					# 	print 'val before = ' + str(val_before)
					# 	if max_score:
					# 		print float(val_before) / float(max_score)


		# Sort and assign positions
		rank_by = conf['rankBy']
		self.ranking = sorted(self.ranking, key=lambda d: d['ranking'][rank_by]['score'], reverse=True)
		self.ranking = Ranker.assign_positions(self.ranking, rank_by)
		# print self.ranking[0]['ranking']
		#  Return copy by value
		r = self.get_ranking()
		print "Ranker: returns " + str(len(r))
		print r[0]['ranking']
		return r



	@staticmethod 
	def are_features_empty(features):
		for fvalues in features.values():
			if len(fvalues):
				return False
		return True



	@staticmethod
	def normalize_score(x, max_x):
		#  assume min = 0
		value = float(x) / float(max_x) if max_x else 0.0
		# print 'x = ' + str(x) + ', max_x = ' + str(max_x) + ', div = ' + str(value)
		if max_x:
			return float(x) / float(max_x)
		return 0.0



	def get_ranking(self, offset=0, limit=50):
		limit = offset + limit
		# Return a copy by value
		# return copy.deepcopy(self.ranking[offset:100]) 
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

