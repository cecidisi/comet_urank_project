# from comet_urank.classes.ranking import *
from comet_urank.models import *
from comet_urank.classes.db_connector import *
from comet_urank.classes.ranker import *
import json

ranker = Ranker()

class Urank:

	def __init__(self):
		# documents
		self.documents = []
		self.docs_to_send = []
		self.doc_offset = 0
		self.doc_limit = 50
		# document features
		self.doc_keywords = []
		self.doc_tags = []
		# keywords
		self.keywords = []
		self.keywords_to_send = []
		self.usertags = []
		self.kw_offset = 0
		self.kw_limit = 100
		self.ranking =  []
		self.attr_remove = ['keywords_str', 'tags_str']
		# set on update
		self.rs_conf = {}
		self.query = []
		self.utags = []


	@staticmethod
	def get_obj_remove_field(obj, targets):
		map(obj.pop, targets)
		return obj
		# return [{i:obj[i] for i in obj if i not in targets}]


	@staticmethod
	def get_documents_to_send(documents, offset, limit, doc_tags, attr_remove):
		docs_to_send = documents[offset:limit]
		# self.docs_to_send = [dict(item, **{'tags' : item['tags_str'].split()}) if d['tags_str'] is not None else item for item in self.docs_to_send]
		# self.docs_to_send = [urank_handler.get_obj_remove_field(d, attr_remove) for d in self.docs_to_send]
		for i, d in enumerate(docs_to_send):
			d['tags'] = doc_tags[i+offset]
			# d['keywords'] = self.doc_keywords[i+self.doc_offset]
			map(d.pop, attr_remove)
		return docs_to_send

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
		for stem, color in kw_colors.iteritems():
			positions = doc_keywords[stem][pos_attr] if stem in doc_keywords else []
			for pos in positions:
				word = text[pos['from']:pos['to']]
				highlights.append({
					'word': Urank.get_formatted_word(word, color, decoration),
					'from': pos['from'],
					'to': pos['to']
				})
		highlights = sorted(highlights, key=lambda h: h['to'])
		last_pos = len(text)
		# Go backwards replacing text
		for h in highlights[::-1]:
			text_after = text[h['to'] : last_pos]
			pretty_text = h['word'] + text_after + pretty_text
			last_pos = h['from']

		return text[0:last_pos] + pretty_text




	def load_documents(self, documents):		
		self.documents = documents
		print 'urank: I have ' + str(len(self.documents)) + ' documents'
		self.doc_keywords = [json.loads(d['keywords_str']['keyword_str']) for d in self.documents ]		
		self.doc_tags = [d['tags_str']['tag_str'].split() if d['tags_str'] else [] for d in self.documents ]    
		ranker.set_data(self.documents, self.doc_keywords, self.doc_tags)

		self.docs_to_send = Urank.get_documents_to_send(self.documents, self.doc_offset, self.doc_limit, self.doc_tags, self.attr_remove)
		print 'urank: Sending ' + str(len(self.docs_to_send)) + ' documents'
		return self.docs_to_send


	def load_keywords(self, keywords):
		self.keywords = keywords
		print 'urank: Loaded ' + str(len(self.keywords)) + ' keywords'
		self.keywords_to_send = self.keywords[self.kw_offset:self.kw_limit]
		print 'urank: Sending ' + str(len(self.keywords_to_send)) + ' keywords'
		return self.keywords_to_send


	def load_usertags(self, usertags):
		print 'urank: Received ' + str(len(usertags)) + ' usertags'
		self.usertags = usertags
		return self.usertags	


	def process_operation(self, params):
		operation = params['operation']
	    
	    # UPDATE RANKING
		if operation == 'update':
			self.rs_conf = params['rs_conf'] or {}
			self.query = params['query'] or []
			self.utags = params['utags'] or []
			self.ranking = ranker.update(self.rs_conf, self.query, self.utags)
			self.doc_offset = 0
			# print self.ranking[0]['ranking']
			return self.ranking[self.doc_offset:self.doc_limit]
		
		# CLEAR RANKING
		elif operation == 'clear':
			return ranker.clear()
		
		# SEND MORE DOCUMENTS
		elif operation == 'show_more':
			self.doc_offset += self.doc_limit
			print 'Returning documents from '+str(self.doc_offset)+' to '+str(self.doc_offset+self.doc_limit)
			return ranker.get_ranking(self.doc_offset, self.doc_offset+self.doc_limit)
		
		# GET DOCUMENT DETAILS
		#  query and utags have assigned colors!!
		elif operation == 'get_document_details':
			doc_id = params['doc_id'] or None
			idx = params['doc_index'] or None
			decoration = params['decoration'] if params['decoration'] else 'background'
			if idx is not None:
				print 'Index = ' + str(idx)
				doc = self.documents[idx]
				kw_colors = {}
				for k in self.query:
					kw_colors[k['stem']] = k['color']
				doc['pretty_title'] = Urank.get_formatted_text(doc['title'], self.doc_keywords[idx], 'pos_title', kw_colors, decoration)  
				print doc['pretty_title']
				doc['pretty_detail'] = Urank.get_formatted_text(doc['detail'], self.doc_keywords[idx], 'pos_detail', kw_colors, decoration)  
				# print doc['pretty_detail']
				return doc
			return {}

















