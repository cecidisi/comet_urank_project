from functools import reduce
import collections
from collections import Counter
import re
import time
import nltk
from nltk import word_tokenize
from nltk.corpus import words, stopwords, brown
from nltk.util import ngrams
from .tfidf import *

wnl = nltk.WordNetLemmatizer()
stemmer = nltk.PorterStemmer()
tfidf = TfIdf()

default_options = {
	'stopwords': [],
	'title_weight' : 1,
	'abstract_weight' : 0.2,
	'min_word_length': 3,
	'min_rep_global_keyword' : 3,
	'max_length_keyphrase': 3,
	'min_rep_keyphrase' : 1,
	'doc_keywords_only': False
}

class keyword_extractor:

	def __init__(self, options=None):
		self.documents = []			# { id, title, abstract }
		self.documents_keywords = []		# { id, terms: [key]: { tf (obj, pos (arr) } }
		self.all_tokens = {}
		self.stem_variations = {}
		self.terms_to_stems = {}
		self.keyphrases = {}
		self.stem_to_phrases = {}
		self.global_keywords = []	# { id, term, appears_in (arr), keyphrases }
		options = options or {}
		self.opt = dict(default_options, **options)
		self.stopwords = set(nltk.corpus.stopwords.words('english') + self.opt['stopwords'])
		print self.opt['doc_keywords_only']


	@staticmethod
	def _get_tokens(text, stopwords):
		# Tokenize
		tokens = word_tokenize(text)
		tokens = [t.lower() for t in tokens if t.isalpha() and t.lower() not in stopwords]
		# POS Tagging
		tagged = nltk.pos_tag(tokens)
		# Filter and Stem
		filtered = []
		stemmed = []
		for t in tagged:
			if t[1] == 'NN':
				filtered.append(t[0])
				stemmed.append(stemmer.stem(t[0]))
			elif t[1] == 'NNS':
				# Add term in plural
				filtered.append(t[0])
				# Lemmatize then stem
				stemmed.append(stemmer.stem(wnl.lemmatize(t[0]))) 

		return { 'raw': tokens, 'filtered': filtered, 'stemmed': stemmed }


	@staticmethod
	def _is_good_token(tagged):
		return tagged[1] == 'NN'


	@staticmethod
	def _get_kw_pos_in_text(text, filtered, stemmed):
		positions = {}
		word = ''
		# for i, ch in enumerate([c for c in str(text)+'.']):
		for i, ch in enumerate([c for c in text+'.']):
			if ch.isalpha():
				word += ch
			else:
				# print '*** Word after else = ' + word
				if word.lower() in filtered:
					idx = filtered.index(word.lower())
					stem = stemmed[idx]
					# Add entry in positions dict for stem if not exist
					if stem not in positions:
						positions[stem] = []
					positions[stem].append({
						'from': i - len(word),
						'to': i
					})
					# from_i = positions[stem]['from']
					# to_i = positions[stem]['to']
					# print 'stem = ' + stem + 'from: '+ str(from_i) +', to: ' + str(to_i)
					# print 'testing --> ' + text[from_i:to_i]
				word = ''
		return positions
		

	@staticmethod
	def _get_doc_keywords(documents, options, stopwords):
		print 'Start extracting document keywords ...'
		documents_keywords = []
		all_tokens = { 'raw' : [], 'filtered': [], 'stemmed': [] }

		for d in documents:
			# print '1st loop, doc ' + str(d['id'])
			tokens_title = keyword_extractor._get_tokens(d['title'], stopwords)
			tokens_abstract = keyword_extractor._get_tokens(d['abstract'], stopwords)
			stemmed_tokens =  tokens_title['stemmed'] + tokens_abstract['stemmed']
			tfidf.add_document(stemmed_tokens)

			d['positions'] = {
				'title': keyword_extractor._get_kw_pos_in_text(d['title'], tokens_title['filtered'], tokens_title['stemmed']),
				'abstract': keyword_extractor._get_kw_pos_in_text(d['abstract'], tokens_abstract['filtered'], tokens_abstract['stemmed'])
			}

			all_tokens['raw'] += tokens_title['raw'] + ['.'] + tokens_abstract['raw']
			all_tokens['filtered'] += tokens_title['filtered'] + tokens_abstract['filtered']
			all_tokens['stemmed'] += tokens_title['stemmed'] + tokens_abstract['stemmed']

		for idx, d in enumerate(documents):
			n_title = len(tokens_title['stemmed'])
			doc_kw = {}
			for item in tfidf.list_terms(idx):
				stem = item['term']
				is_title =  False   #True if stem in tokens_title['stemmed'] else False
				term_weight = 1     #options['title_weight'] if is_title else options['abstract_weight']
				doc_kw[stem] = {
					'tfidf': item['tfidf'],
					'tf': item['tf'],
					'score': item['tfidf'] * term_weight,
					'is_title' : is_title,
					'pos_title' : d['positions']['title'][stem] if stem in d['positions']['title'] else None,
					'pos_abstract': d['positions']['abstract'][stem] if stem in d['positions']['abstract'] else None
				}
				# if stem == 'prefer':
				# 	print doc_kw[stem]
			documents_keywords.append(doc_kw)
			print 'Got keywords for document #'+str(idx)
		return (documents_keywords, all_tokens)
		

	@staticmethod
	def _get_terms_to_stems_links(terms, stems):
		terms_to_stems = {}
		stem_variations = {}
		for idx, term in enumerate(terms):
			stem = stems[idx]
			# update terms_to_stems dictionary
			if term not in terms_to_stems:
				terms_to_stems[term] = stem
			#  update stem_variations dictionary
			if stem not in stem_variations:
				stem_variations[stem] = {}
				# continue
			if term not in stem_variations[stem]:
				stem_variations[stem][term] = { 'count': 0 }
				# continue
			stem_variations[stem][term]['count'] += 1
		print 'Finished linking terms and stems'
		return (terms_to_stems, stem_variations)



	@staticmethod
	def _get_keyphrases(raw_tokens, terms_to_stems, options):
		min_gram = 2
		max_gram = options['max_length_keyphrase']
		min_rep = options['min_rep_keyphrase']

		keyphrases = {}
		stem_to_phrases = {}
		for n in range(min_gram, max_gram):
			n_grams = ngrams(raw_tokens, n)
			counter = collections.Counter(n_grams)
			for val, count in counter.most_common():
				if n == len([t for t in val if t in terms_to_stems ]): # number of terms with keyword stem
					phrase = ' '.join(val)
					sequence = [ [{ 'term': term, 'stem': terms_to_stems[term] }] for term in val ]
					if phrase not in keyphrases:
						keyphrases[phrase] = { 'phrase': phrase, 'sequence': sequence, 'count': 0 }
					keyphrases[phrase]['count'] += 1					
					# add entries for each term's stem in keyphrases
					for term in val:
						stem = terms_to_stems[term]
						if stem not in  stem_to_phrases:
							stem_to_phrases[stem] = {}
						if phrase not in stem_to_phrases[stem]:
							stem_to_phrases[stem][phrase] = True

		print 'Finished processing keyphrases'
		filtered_keyphrases = [kp for key, kp in keyphrases.iteritems() if kp['count'] >= min_rep]
		return (filtered_keyphrases, stem_to_phrases)

	# variations = dict of { term: count }
	@staticmethod
	def _get_best_term(stem, variations):
		if len(variations) == 0:
			return False
		# Only one variations
		if len(variations) == 1:
			return variations.keys()[0]
		# 2 variations, one in lower case and the other starting in uppercase --> return in lower case
		# if (len(variaitons) == 2 and !keys[0].isAllUpperCase() && !keys[1].isAllUpperCase() && keys[0].toLowerCase() == keys[1].toLowerCase())
		# 	return keys[0].toLowerCase();
		# One variation is repeated >= 70%
		counts = [v['count'] for term, v in variations.iteritems()]
		tot_count = reduce((lambda x, y: x + y), counts) if len(counts) else 0
		freq_term = [term for term, v in variations.iteritems() if v['count'] > (0.7 * tot_count) ] 
		if len(freq_term):
			return freq_term[0]
		# One variation ends in '-ion', '-ment', '-ism' or '-ty'
		p = re.compile('ion$|ment$|ty$|ism$')
		noun_endings =  [term for term in variations if p.search(term)]
		if len(noun_endings):
			return noun_endings[0]
		# One variation matches stem inv ariations dict
		if stem in variations:
			return stem
		# Pick shortest variation. Sort by term length, then return term in first tuple, i.e. [0][0]
		short_terms = sorted([(term, len(term)) for term, v in variations.iteritems()], key=lambda k: k[1])
		return short_terms[0][0]


	
	@staticmethod
	def _get_global_keywords(stem_variations, documents, options):
		min_df = options['min_rep_global_keyword']
		min_word_length = options['min_word_length']
		keywords_dict = {}
		for stem, item in tfidf.get_term_info().iteritems():
			# Filter out words that don't meet minimum df and stem length
			if item['df'] >= min_df and len(stem) > min_word_length:
				keywords_dict[stem] = {
					'stem': stem, 
					'term': keyword_extractor._get_best_term(stem, stem_variations[stem] ),
					'df': item['df'],
					'entropy': item['entropy'],
					'score':item['df'],
					'variations': sorted([{ 'term': key, 'count': val } for key, val in stem_variations[stem].iteritems() ], key=lambda k: k['count'], reverse=True ), 
					'appears_in' : [d['id'] for i, d in enumerate(documents) if i in item['documents_idx']]
				}
				print 'Got keyword "' + stem + '"'

		global_keywords = sorted([value for key, value in keywords_dict.iteritems()], key=lambda k: k['df'], reverse=True)
		return global_keywords
	

	#  INSTANCE METHODS
	def add_document(self, doc):
		title = doc['title'] or doc['text']
		abstract = doc['abstract'] or ''
		self.documents.append({
			'id': doc['id'], 
			'title': title, 
			'abstract': abstract, 
			# 'text': str(title)+'\n'+str(abstract)
			'text': title + '\n' + abstract
		})
		print 'Added document #'+str(doc['id'])


	def extract(self):
		print 'Start keyword extraction'
		tfidf.clear()
		start_time = time.time()
		self.documents_keywords, self.all_tokens = keyword_extractor._get_doc_keywords(self.documents, self.opt, self.stopwords)
		if not self.opt['doc_keywords_only']:
			self.terms_to_stems, self.stem_variations = keyword_extractor._get_terms_to_stems_links(self.all_tokens['filtered'], self.all_tokens['stemmed'])
			self.keyphrases, self.stem_to_phrases = keyword_extractor._get_keyphrases(self.all_tokens['raw'], self.terms_to_stems, self.opt)
			self.global_keywords = keyword_extractor._get_global_keywords(self.stem_variations, self.documents, self.opt)
		end_time = time.time()
		print 'Finished keyword extraction (' + str(end_time - start_time) + ' ms)'

	def get_document_keywords(self, idx):
		return self.documents_keywords[idx]


	def get_global_keywords(self):
		return (self.global_keywords)

	def get_keyphrases(self):
		return (self.keyphrases, self.stem_to_phrases)

