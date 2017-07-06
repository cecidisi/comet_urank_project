from math import log

class TfIdf():

	def __init__(self):
		self.clear();
		

	def clear(self):
		self.documents = []
		self.tf = []	 # doc_idx -> { term : tf }
		self.term_info = {}  # { df: num, entropy: num} per term entry
		self.df = {} 	 # term -> { df, documents_idx}
		self.total_terms = 0

	def add_document(self, doc):
		self.documents.append(doc)
		doc_idx = len(self.documents)
		doc_tf = {}
		unique_terms_in_doc = {}
	
		for term in doc:	
			# update term freq. for current doc
			if term not in doc_tf:
				doc_tf[term] = 0
			doc_tf[term] += 1
			# df, prob and entropy for term in collection
			if term not in self.term_info:
				self.term_info[term] = { 'df': 0, 'prob': 0, 'entropy': 0, 'documents_idx': []}
			if term not in unique_terms_in_doc:
				self.term_info[term]['df'] += 1
				self.term_info[term]['documents_idx'].append(doc_idx)
				unique_terms_in_doc[term] = True
			#  used to compute entropy later
			self.term_info[term]['prob'] += 1
			self.total_terms += 1

		self.tf.append(doc_tf)

		# # update doc freq. for current tag
		# unique_terms = set(doc)
		# for term in unique_terms:
		# 	if term not in self.df:
		# 		self.df[term] = { 'df' : 0, 'documents_idx': [] }
		# 	self.df[term]['df'] += 1
		# 	self.df[term]['documents_idx'].append(doc_idx)


	def list_terms(self, idx):
		tfidf_list = []
		for term, tf in self.tf[idx].iteritems():
			# tfidf = float(tf) / float(self.df[term]['df'])
			tfidf = float(tf) / float(self.term_info[term]['df'])
			# print 'tfidf = ' + str(tfidf) + ', tf = ' + str(tf) + ', df = ' + str(self.df[term]['df'])
			tfidf_list.append({ 'term': term, 'tfidf': tfidf, 'tf': tf })

		return sorted(tfidf_list, key=lambda k: k['tfidf'])


	def get_term_info(self): 
		for term, value in self.term_info.iteritems():
			prob = value['prob'] / float(self.total_terms)
			value['entropy'] = -(prob * log(prob))
		return self.term_info











