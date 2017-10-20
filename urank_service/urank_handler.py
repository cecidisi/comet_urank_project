
import json
from .ranker import *


ranker = Ranker()

class Urank:

	def __init__(self, options = {}):
		
		self.opt = {
			'num_documents': 50,
			'num_keywords': 100,
			'num_neighbors': 50
		}
		self.opt.update(options)
		self.clear()



	def clear(self):
		# documents
		self.documents = []
		# self.docs_to_send = []
		self.doc_offset = 0
		self.doc_limit = self.opt['num_documents']
		# document features
		self.doc_id_to_index = {}
		self.doc_keywords = []
		self.doc_tags = []
		# keywords
		self.keywords = []
		self.kw_offset = 0
		self.kw_limit = self.opt['num_keywords']
		# usertags
		self.usertags = []
		# neighbors
		self.neighbors = []
		self.nb_offset = 0
		self.nb_limit = self.opt['num_neighbors']
		# set on update
		self.rs_conf = {}
		self.query = []
		self.utags = []
		self.kw_colors = {}

		ranker.clear()


	# STATIC METHODS
	@staticmethod
	def get_obj_remove_field(obj, targets):
		map(obj.pop, targets)
		return obj
		# return [{i:obj[i] for i in obj if i not in targets}]



	@staticmethod
	def get_formatted_word(word, color, decoration):
		if decoration == 'background':
			return "<strong style='border-radius: 4px; font-weight: normal; border: 1px solid "+ color +";background:" + color + "'>" + word + "</strong>"
		else:
			return "<strong style='border-bottom: 1px solid " + color + "'>" + word + "</strong>"


	@staticmethod
	def get_formatted_text(text, doc_keywords, pos_attr, kw_colors, decoration):
		pretty_text = ''
		highlights = []
		# Add all formatted words to highlights list and then sort from last to first
		for stems, color in kw_colors.iteritems():
			for stem in stems.split(' '):
				# Positions for current keyword
				positions = doc_keywords[stem][pos_attr] if stem in doc_keywords else []
				for pos in positions:
					word = text[pos['from']:pos['to']]
					highlights.append({
						'styled_word': Urank.get_formatted_word(word, color, decoration),
						'from': pos['from'],
						'to': pos['to']
					})
		# Sort all highlights from last to first
		highlights = sorted(highlights, key=lambda h: h['to'])
		last_pos = len(text)
		# Go backwards replacing text
		for h in highlights[::-1]:
			text_after = text[h['to'] : last_pos]
			pretty_text = h['styled_word'] + text_after + pretty_text
			last_pos = h['from']

		return text[0:last_pos] + pretty_text



	# INSTANCE METHODS
	def load_documents(self, documents):		
		self.documents = documents
		print 'urank: Loaded ' + str(len(self.documents)) + ' documents'		
		self.doc_tags = []
		self.keywords = []
		for idx, d in enumerate(self.documents):
			self.doc_keywords.append(d['keywords'])
			d.pop('keywords', None)
			self.doc_id_to_index[d['id']] = idx

		ranker.set_data(self.documents)
		ranker.load_doc_keywords(self.doc_keywords)
		docs_to_send = ranker.get_ranking()[self.doc_offset:self.doc_limit]
		print 'urank: Sending ' + str(len(docs_to_send)) + ' documents'
		print docs_to_send[0]
		return docs_to_send


	def load_keywords(self, keywords):
		self.keywords = keywords
		print 'urank: Loaded ' + str(len(self.keywords)) + ' keywords'
		keywords_to_send = self.keywords[self.kw_offset:self.kw_limit]
		print 'urank: Sending ' + str(len(keywords_to_send)) + ' keywords'
		print keywords_to_send[0]
		return keywords_to_send


	def load_usertags(self, usertags):
		print 'urank: Received ' + str(len(usertags)) + ' usertags'
		self.usertags = usertags
		return self.usertags	


	def load_neighbors(self, neighbors, sim_user_talk):
		print 'urank: Received ' + str(len(neighbors)) + ' neighbors'
		self.neighbors = ranker.load_neighbors(neighbors, sim_user_talk)
		# ranker.load_sim_item_user(sim_user_talk)
		neighbors_to_send = self.neighbors[self.nb_offset : self.nb_limit]
		print 'urank: Sending ' + str(len(neighbors_to_send)) + ' neighbors'
		return neighbors_to_send


	def get_document_details(self, doc, decoration):
		doc_kw = self.doc_keywords[ self.doc_id_to_index[doc['id']] ]
		doc['title'] = Urank.get_formatted_text(doc['title'], doc_kw, 'pos_title', self.kw_colors, decoration)
		print doc['title']				
		doc['abstract'] = Urank.get_formatted_text(doc['abstract'], doc_kw, 'pos_detail', self.kw_colors, decoration)
		return doc
		


	def process_operation(self, params):
		operation = params['operation']
	    
	    # UPDATE RANKING
		if operation == 'update':
			self.doc_offset = 0
			self.rs_conf = params['rs_conf'] if 'rs_conf' in params else {}
			self.features = params['features'] if 'features' in params else {}
			# self.query = params['query'] or []
			# self.utags = params['utags'] or []

			ranker.update(self.rs_conf, self.features)
			docs_to_send = ranker.get_ranking()[self.doc_offset:self.doc_limit]
			# Prepare docs to send with pretty titles
			self.kw_colors = {}
			for k in self.features['keywords']:
				self.kw_colors[k['stem']] = k['color']
			# print self.kw_colors
			decoration = params['decoration'] or 'word'
			# print docs_to_send[0]['title']
			for idx, doc in enumerate(docs_to_send):
				doc_kw = self.doc_keywords[ self.doc_id_to_index[doc['id']] ]
				doc['title'] = Urank.get_formatted_text(doc['title'], doc_kw, 'pos_title', self.kw_colors, decoration)  
			# print docs_to_send[0]['title']
			print 'Sending ranking with ' + str(len(docs_to_send)) + ' documents'
			return docs_to_send
		

		# CLEAR RANKING
		elif operation == 'clear':
			return ranker.clear()
		

		# SEND MORE DOCUMENTS
		elif operation == 'show_more':
			self.doc_offset += self.doc_limit
			print 'Returning documents from '+str(self.doc_offset)+' to '+str(self.doc_offset+self.doc_limit)
			return ranker.get_ranking(self.doc_offset, self.doc_limit)
		

		# GET DOCUMENT DETAILS
		#  query and utags have assigned colors!!
		elif operation == 'get_document_details':
			doc_id = params['doc_id'] # if params['doc_id'] else None
			idx = params['doc_index'] # if params['doc_index'] else -1
			decoration = params['decoration'] if params['decoration'] else 'background'
			print 'index = ' + str(idx)
			print 'id = ' + str(doc_id)
			if idx > -1:
				doc = ranker.get_item(idx)
				doc_kw = self.doc_keywords[ self.doc_id_to_index[doc_id] ]
				doc['title'] = Urank.get_formatted_text(doc['title'], doc_kw, 'pos_title', self.kw_colors, decoration)
				print doc['title']				
				doc['abstract'] = Urank.get_formatted_text(doc['abstract'], doc_kw, 'pos_detail', self.kw_colors, decoration)
				print doc['abstract']
				return doc
			return {}

















