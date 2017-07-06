import math
from functools import reduce
	
class RSContentBased:

	
	@staticmethod
	def get_eucliden_norm(doc_keywords):
		acum_squares = 0
		for key, k in doc_keywords.iteritems():
			acum_squares += pow(k['tfidf'], 2)
		
		return math.sqrt(float(acum_squares))


	@classmethod
	def get_CB_score(cls, doc_keywords, query, cb_weight):
		total_score = 0
		max_score = 0
		term_scores = []
		doc_norm = RSContentBased.get_eucliden_norm(doc_keywords)
		unit_query_vec_dot = 1.00 / float(math.sqrt(len(query)))
		for q in query:
			stem = q['stem']
			weight = q['weight']
			term_score = (doc_keywords[stem]['tfidf'] / doc_norm) * unit_query_vec_dot * float(weight) * float(cb_weight) if stem in doc_keywords else 0
			term_score = round(term_score, 3)
			total_score += term_score
			max_score = max(term_score, max_score)
			term_scores.append({ 'term': q['term'], 'stem': stem, 'score': term_score })
		return { 'score' : total_score, 'max_score': max_score, 'term_scores': term_scores }


		# if query and len(query):
		# 	is_one = False if isinstance(data, list) else True
		# 	if is_one:
		# 		data = [data]
			
		# 	for d in data:
		# 		d['ranking']['cbScore'] = 0
		# 		d['ranking']['cbMaxScore'] = 0
		# 		d['ranking']['cbKeywords'] = []
		# 		doc_norm = get_eucliden_norm(doc_keywords)
		# 		unit_query_vec_dot = 1.00 / float(math.sqrt(len(query)))
		# 		_max = 0
		# 		for q in query:
		# 			stem = q['stem']
		# 			weight = q['weight']
		# 			# termScore = tf-idf(d, t) * unitQueryVector(t) * weight(query term) / |d|   ---    |d| = euclidenNormalization(d)
		# 			term_score = (doc_keywords[stem]['tfidf'] / doc_norm) * unit_query_vec_dot * float(weight) * float(cb_weight) if stem in doc_keywords else 0.0
		# 			d['ranking']['cbScore'] = term_score
		# 			d['ranking']['cbMaxScore'] = max(term_score, d['ranking']['cbMaxScore'])
		# 			d['ranking']['cbKeywords'].append({ 'term': q['term'], 'stem': stem, 'weightedScore': term_score })

		# 	return data if not is_one else data[0]

