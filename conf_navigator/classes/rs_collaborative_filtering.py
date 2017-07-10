import math
from functools import reduce
	
class RSCollaborativeFiltering:

	def __init__(self):
		self.max_score = 0.0
		self.sim_v = {}
		self.sim_iv = {}
	

	def set_sim_v(self, sim_v):
		self.sim_v = sim_v


	def set_sim_iv(self, sim_iv):
		self.sim_iv = sim_iv


	def clear(self):
		self.max_score = 0.0

	def get_max_score(self):
		return self.max_score


	def get_score(self, idx, doc_id, params, conf):
		neighbors = params['neighbors']
		cf_weight = conf['weight']
		total_score = 0
		v_scores = []
		# print 'CF weight = ' + str(cf_weight)
		for v in neighbors:
			vid = v['id']
			# print 'doc id = '+ str(doc_id) + '; vid = ' + str(vid)
			if doc_id in self.sim_iv:
				if vid in self.sim_iv[doc_id]:
					print 'string vid, score = ' + str(self.sim_iv[doc_id][vid])
				elif int(vid) in self.sim_iv[doc_id]:
					print 'int vid, score = ' + str(self.sim_iv[doc_id][int(vid)])					
			
			# print self.sim_iv[doc_id] if doc_id in self.sim_iv else 'no entries'

			vweight = v['weight']
			sim_neighbor_item = 0.0
			if doc_id in self.sim_iv and vid in self.sim_iv[doc_id]:
				sim_neighbor_item = self.sim_iv[doc_id][vid]	
			# score = self.sim_v[vid] * sim_neighbor_item
			score = sim_neighbor_item #* cf_weight
			# print str(sim_neighbor_item) + ' -- ' + str(score)
			total_score += score
			# v_scores.append({ 'vid': vid, 'score': score })
			v_scores.append({ 'id': vid, 'name': v['name'], 'score': score })
		self.max_score = max(total_score, self.max_score)
		return { 'score' : total_score, 'details': v_scores }


