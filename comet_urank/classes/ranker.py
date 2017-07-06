from comet_urank.classes.rs_content_based import *

class Ranker:

	def __init__(self):
		self.clear()


	@staticmethod
	def assign_positions(ranking, score):
		cur_score = float('inf')
		cur_pos = 1
		items_in_cur_pos = 0
		for d in ranking:
			if d['ranking'][score]:
				if d['ranking'][score] < cur_score:
					cur_pos = cur_pos + items_in_cur_pos
					cur_score = d['ranking'][score]
					items_in_cur_pos = 1
				else:
					items_in_cur_pos +=1
				d['ranking']['pos'] = cur_pos
			else:
				d['ranking']['pos'] = 0
			# compute shift
			d['ranking']['pos_changed'] = d['ranking']['prev_pos'] - d['ranking']['pos'] if d['ranking']['prev_pos'] else 1000
		return ranking



	def set_data(self, data, doc_keywords, doc_tags):
		self.data = data
		for idx, d in enumerate(self.data): 
			d['idx'] = idx
			d['ranking'] = {
				'pos': 0,
				'pos_changed': 0,
				'prev_pos': 0
			}
		self.ranking = self.data[:]
		self.doc_keywords = doc_keywords
		self.doc_tags = doc_tags


	def update(self, conf, query, utags):
		print [(q['stem'], q['weight']) for q in query]
		cb_weight = conf['CB']['weight']
		tu_weight = conf['TU']['weight']
		rank_by = conf['rankBy']
		score =  conf[rank_by]['name']
		if len(query):
			for d in self.ranking:
				idx = d['idx']
				d['ranking']['prev_pos'] = d['ranking']['pos']
				if cb_weight:
					cb_resp = RSContentBased.get_CB_score(self.doc_keywords[idx], query, cb_weight)
					d['ranking']['cb_score'] = cb_resp['score']
					d['ranking']['cb_max_score'] = cb_resp['max_score']
					d['ranking']['cb_details'] = cb_resp['term_scores']

				d['ranking']['total_score'] = d['ranking']['cb_score']
			self.ranking =  sorted(self.ranking, key=lambda d: d['ranking'][score], reverse=True)
			self.ranking = Ranker.assign_positions(self.ranking, score)
			return self.ranking
		else:
			self.ranking = self.data[:]
			return self.ranking


	def get_ranking(self, offset=0, limit=50):
		return self.ranking[offset:limit]
		

	def clear(self):
		self.data = []
		self.doc_keywords = []
		self.doc_tags = []
		self.ranking = []
		self.query = []
		return self.ranking

