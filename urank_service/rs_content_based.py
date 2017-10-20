import math
from functools import reduce
	
class RSContentBased:

	def __init__(self):
		self.max_score = 0.0

	
	def clear(self):
		self.max_score = 0.0


	def set_doc_keywords(self, doc_keywords):
		self.doc_keywords = doc_keywords


	def get_max_score(self):
		return self.max_score


	def get_score(self, idx, doc_id, params, conf):
		query = params['keywords']
		cb_weight = conf['weight']
		doc_kw = self.doc_keywords[idx]
		total_score = 0
		term_scores = []
		doc_norm = RSContentBased.get_eucliden_norm(doc_kw)
		unit_query_vec_dot = 1.00 / float(math.sqrt(len(query))) if len(query) else 0.0
		for q in query:
			stems = q['stem'].split(' ')
			weight = q['weight']
			# term_score = (doc_kw[stem]['tfidf'] / doc_norm) * unit_query_vec_dot * float(weight) * float(cb_weight) if stem in doc_kw else 0.0
			term_score = 0
			# Check that a document contains all stems
			if all(s in doc_kw.keys() for s in stems):
				for stem in stems:
					term_score += (doc_kw[stem]['tfidf'] / doc_norm) * unit_query_vec_dot * float(weight) \
						if stem in doc_kw \
						else 0.0
				total_score += term_score
			# term_scores.append({ 'term': q['term'], 'stem': stem, 'score': term_score })
			term_scores.append({ 'id': q['id'], 'name': q['name'], 'score': term_score })
		self.max_score = max(total_score, self.max_score)
		return { 'score' : total_score, 'details': term_scores }


	@staticmethod
	def get_eucliden_norm(doc_keywords):
		acum_squares = 0
		for key, k in doc_keywords.iteritems():
			acum_squares += pow(k['tfidf'], 2)
		
		return math.sqrt(float(acum_squares))






