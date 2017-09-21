from math import log

class TfIdf():

	def __init__(self):
		self.clear();
		

	def clear(self):
		self.documents = []
		self.tf = []	 # doc_idx -> { term : tf }
		self.term_info = {}  # { df: num, entropy: num} per term entry
		self.total_terms = 0
		self.max_ctf = 0.0 # max corpus tf


	def add_document(self, doc):
		self.documents.append(doc)
		doc_idx = len(self.documents)
		doc_tf = {}
		unique_terms_in_doc = {}
	
		for term in doc:	
			# update term freq. for current doc
			if term not in doc_tf:
				doc_tf[term] = 0.0
			doc_tf[term] += 1.0 #/ float(len(doc))

			# df, prob and entropy for term in collection
			if term not in self.term_info:
				self.term_info[term] = { 'df': 0, 'ctf': 0, 'prob': 0, 'entropy': 0, 'documents_idx': []}
			
			if term not in unique_terms_in_doc:
				self.term_info[term]['df'] += 1
				self.term_info[term]['documents_idx'].append(doc_idx)
				unique_terms_in_doc[term] = True
			
			#  used to compute entropy later
			self.term_info[term]['prob'] += 1
			self.term_info[term]['ctf'] += 1
			self.max_ctf = self.term_info[term]['ctf'] if self.term_info[term]['ctf'] > self.max_ctf else self.max_ctf
			self.total_terms += 1
		
		self.tf.append(doc_tf)



	def list_terms(self, idx):
		tfidf_list = []
		for term, tf in self.tf[idx].iteritems():
			tfidf = float(tf) / float(self.term_info[term]['df'])

			tfidf_list.append({ 
				'term': term, 
				'tfidf': tfidf, 
				'tf': tf,
				'log_tfidf': log(tfidf)
			})

		return sorted(tfidf_list, key=lambda k: k['tfidf'])


	def get_term_info(self):
		log_max_ctf = log(self.max_ctf, 10)
		print 'max ctf = ' + str(self.max_ctf) #+ ' -- max log ctf = ' + str(log_max_ctf)
		for term, value in self.term_info.iteritems():
			value['term'] = term
			# entropy
			prob = value['prob'] / float(self.total_terms)
			value['entropy'] = -(prob * log(prob))
			# commonness
			value['log_ctf'] = log(value['ctf'], 10)
			value['commonness'] = float(value['log_ctf'] / log_max_ctf)
			value['comm_idx'] = abs(value['commonness'] - 0.5) / 0.5
		return self.term_info











