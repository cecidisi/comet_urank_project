# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from functools import reduce
import collections
from collections import Counter
import json
import re
import time
import nltk
import itertools
import string
from nltk import word_tokenize, Tree
import nltk.tag.util
from nltk.corpus import words, brown
from nltk.util import ngrams
from itertools import izip, groupby, chain
from helper.mp_parallelizer import *
from nlp.tfidf import *
from nlp.stopwords import *
from helper.bcolors import *
from helper.mp_progress_tracker import *
from helper.pretty_time import *
from upmc.models import *

import multiprocessing as mp
from django import db


def save_document_keywords(dpk_kws):
	dpk, kws = dpk_kws
	doc_kws = PubmedDocKeywords(
		keywords = kws['keywords'],
		pos_title = kws['pos_title'] if kws['pos_title'] else {},
		pos_detail = kws['pos_detail'] if kws['pos_detail'] else {}
	)
	doc_kws.save()
	article = Article.objects.get(pk=dpk)
	article.doc_keywords = doc_kws
	article.save()
	return doc_kws.pk



def save_global_keywords(gk):
	global_keyword = PubmedGlobalKeyword(
		stem = gk['stem'],
		term = gk['term'],
		df = gk['df'],
		score = gk['score'],
		variations = gk['variations'],
		num_keyphrases = gk['num_keyphrases']
	)
	global_keyword.save()
	save_keyphrase(gk['phrases'], global_keyword)


def save_keyphrase(phrases, global_keyword):
	for phrase, pos, count, stems in sorted(phrases, key=lambda k:k[2], reverse=True):
		keyphrase = PubmedKeyphrase(
			phrase = phrase,
			pos = pos,
			count = count,
			stems = stems,
			global_keyword = global_keyword
		)
		keyphrase.save()



##### ENTRY POINT

def run():
	time0 = time.time()
	clear()
	articles = Article.objects.all()#[:200]
	print 'Articles retrieved = ' + str(len(articles))
	db.connections.close_all()
	global_keywords, doc_keywords = extract_tfidf(articles)

	print('Extracted ' + str(len(global_keywords))+ ' global keywords')
	print('Extracted ' + str(len(doc_keywords))+ ' document keywords')

	# Save document keywords in parallel
	jobs = Parallelizer.run(save_document_keywords, doc_keywords.iteritems(), db_close=True)
	print('Saved keywords for ' + str(len(jobs)) + ' articles')
	jobs = Parallelizer.run(save_global_keywords, global_keywords)
	print('Saved ' + str(len(jobs)) + ' global keywords')

	# for dpk, kws in doc_keywords.iteritems():
	# 	save_document_keywords((dpk, kws))
	# for gk in global_keywords:
	# 	save_global_keywords(gk)

	print_green('Total time taken = ' + secToMMSS(time.time() - time0))

	# Save top 100 global keywords w/ top 10 phrases to txt file
	import sys
	import os
	with open('upmc/outputs/top_global_keywords.txt', 'w') as f:
		for i, k in enumerate(global_keywords[:100]):
			try:
				f.write(str(i+1) + '. ' + k['term'] + ' -- score = ' + str(k['score']) + '\n')
			except Exception, e:
				print k['term']
			for phrase, pos, count, stems in sorted(k['phrases'], key=lambda k:k[2], reverse=True)[:10]:
				try:
					f.write('\t' + str(phrase) + ' -- ' +str(count) + '\n')
				except Exception, e:
					print phrase

	print 'Saved top 100 global keywords w/ phrases --> "upmc/outputs/top_global_keywords.txt"'
	# extract_textrank()

def clear():
	print_blue('Clearing DB ...')
	PubmedDocKeywords.objects.all().delete()
	PubmedKeyphrase.objects.all().delete()
	PubmedGlobalKeyword.objects.all().delete()
	print_blue('Finished clearing DB ...')


def _lower(word):
	wnl = nltk.WordNetLemmatizer()
	# Trim lower case 's' in acronyms, e.g. AEDs
	word = word[:-1] if word[:-1].isupper() and word[-1] == 's' else word
	# Lowercase trimmed word only if it is not all uppercase or if in lower case not in stopwords
	if not word.isupper() or word.lower() in stopwords:
		return word.lower()
	elif wnl.lemmatize(word.lower()) in stopwords:
		return wnl.lemmatize(word.lower())
	return word

	# return trimmed_word.lower() if not trimmed_word.isupper() else trimmed_word


def _stem(word):
	wnl = nltk.WordNetLemmatizer()
	stemmer = nltk.PorterStemmer()
	# word = _lower(word)
	try:
		return stemmer.stem(word) if len(word) > 3 else word
	except:
		print_red(word)
		return word


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
					'from_pos': i - len(word),
					'to_pos': i
				})
			word = ''
	return positions




def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
 
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass
 
 	return False



def extract_candidate_chunks(text):
	punct = set(string.punctuation)
	# grammar = r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'
	grammar = r'KT: {<JJ>? <NN.*>+}'
	chunker = nltk.chunk.regexp.RegexpParser(grammar)

	tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) 
			for sent in nltk.sent_tokenize(text))

	tagged_words = itertools.chain.from_iterable(tagged_sents)

	all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
		for tagged_sent in tagged_sents))
	
	# key = returned in lambda function: T or F
	candidates = [' '.join(_lower(word) for word, pos, chunk in group)
		for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]

	def _remove_bad_terms(chunk):
		return ' '.join([word for word in chunk.split()
			if len(word) > 2
			and word not in punct
			and not is_number(word)
			])


	filtered = [_remove_bad_terms(cand) for cand in candidates 
		if cand not in stopwords 
		# and not all(char in punct for char in cand) 
		and len(cand.split()) > 1
		and len(cand) > 4
		# and all(len(term) > 3 and term not in punt and not is_number(term) for term in cand)
		]
	return filtered


def extract_tfidf(articles):
	tfidf = TfIdf() # own	
	tmsp = time.time()

	phrase_count = {}
	doc_keywords = {}
	term_positions = {} #in documents
	all_stems = []
	all_terms = []

	print_blue('Extracting chunks, stemming and filtering (1st loop) ... ')
	for i, d in enumerate(articles):
		# print 'Article #' + str(i+1) + '/' + str(len(articles)) + '\n'
		text = d.title + '\n' + d.abstract or ''
		filtered_chunks = extract_candidate_chunks(text)

		filtered_words = [word for phrase in filtered_chunks for word in phrase.split()]
		stemmed_words = [_stem(word) for word in filtered_words]
		all_stems.extend(stemmed_words)
		all_terms.extend(filtered_words) 

		tfidf.add_document(stemmed_words)

		doc_keywords[d.pk] = {
			'keywords': {},  # overwritten in next loop
			'pos_title' : _get_kw_pos_in_text(d.title, filtered_words, stemmed_words),
			'pos_detail': _get_kw_pos_in_text(d.abstract, filtered_words, stemmed_words)
		}

		# collection key phrases
		for k in filtered_chunks:
			phrase_count[k] = 1 if not k in phrase_count else phrase_count[k] + 1

	print_blue('Preparing document keywords (2nd loop) ... ')
	# document single-term keywords
	for idx, d in enumerate(articles):
		kws = {}
		for item in tfidf.list_terms(idx):
			# document term
			stem = item['term']
			log_tfidf = log(item['tfidf'])
			kws[stem] = {
				'stem': stem,
				# 'tfidf': item['tfidf'],
				# 'log_tfidf': item['log_tfidf'],
				'score': item['tfidf']
			}

		doc_keywords[d.pk]['keywords'] = kws


	print_blue('Preparing global keywords and key phrases ... ')
	# collection key phrases from chunks
	term_info = tfidf.get_term_info()

	term_variations = { stem: collections.Counter([k[1] for k in group]).most_common()
		for stem, group in groupby(izip(all_stems, all_terms), lambda k: k[0]) }

	term_phrases = {}
	max_score = 0.0

	for phrase, count in phrase_count.iteritems():
		terms = phrase.split()
		for pos, term in enumerate(terms):
			stem = _stem(term)
			if stem in term_info and term_info[stem]['df'] > 3 and term not in stopwords:
				# freq terms on key phrases
				if stem not in term_phrases:
					term_phrases[stem] = {
						'stem': stem,
						'term': term,
						'df': term_info[stem]['df'],
						'score': term_info[stem]['log_ctf'],
						'variations': ' '.join(k[0] for k in sorted(term_variations[stem], key=lambda k:k[1], reverse=True)),
						'num_keyphrases': 0,
						'phrases': []
					}
					max_score = max(max_score, term_phrases[stem]['score'])
				term_phrases[stem]['num_keyphrases'] += 1
				term_phrases[stem]['phrases'].append((
					phrase,
					pos,
					count,
					' '.join([_stem(word) for word in terms])
				))

	whitelist = ['prophylaxis', 'metoprolol', 'beta-blocker', 'propranolol', 'timolol', 'atenolol',
				'divalproex', 'sodium,' 'valproate', 'topiramate', 'aspirin', 'acetaminophen,' 'prevention']

	def _upgrade_whitelisted(val):
		if val['term'] in whitelist:
			val['score'] = max_score
		return val

	global_keywords = sorted([_upgrade_whitelisted(value) 
		for stem, value in term_phrases.iteritems()], key=lambda k: k['score'], reverse=True)

	print_green('Extraction time = ' + secToMMSS(time.time() - tmsp))
	return global_keywords, doc_keywords








###########################


def extract_candidate_words(text):
	good_tags = ['NN','NNP','NNS','NNPS']
	punct = set(string.punctuation)


	tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent) 
		for sent in nltk.sent_tokenize(text)))

	candidates = [word.lower() for word, tag in tagged_words
		if tag in good_tags and word.lower() not in stopwords
		and not all(char in punct for char in word)
		]

	return candidates




def extract_textrank():
	articles = Article.objects.all()[:1000]
	tmsp = time.time()

	all_texts = []
	for p in articles:
		text = p.title + '\n' + p.abstract or ''
		# keyphrases = score_keyphrases_by_textrank(text, 1)
		# print keyphrases
		all_texts.append(text)


	all_texts = '\n'.join(all_texts)
	all_keyphrases = score_keyphrases_by_textrank(all_texts)
	keyphrases = []
	j = 0
	for i, k in enumerate(all_keyphrases):
		
		punct = set(string.punctuation)
		grammar = r'KT: {<JJ>? <NN.*>+}'
		chunker = nltk.chunk.regexp.RegexpParser(grammar)

		tagged_phrase = nltk.pos_tag_sents(nltk.word_tokenize(sent) 
			for sent in nltk.sent_tokenize(k[0]))

		if len(tagged_phrase) and len(keyphrases) < 201:
			keyphrases.append(k)
			j += 1
			

	for i, k in enumerate(keyphrases):
		print str(i+1) + '. ' + k[0] + ' -- ' + str(round(k[1], 4))








def score_keyphrases_by_textrank(text, n_keywords=0.05):
    from itertools import takewhile, tee, izip
    import networkx, nltk
    
    # tokenize for all words, and extract *candidate* words
    words = [word.lower()
             for sent in nltk.sent_tokenize(text)
             for word in nltk.word_tokenize(sent)]
    candidates = extract_candidate_words(text)
    # build graph, each node is a unique candidate
    graph = networkx.Graph()
    graph.add_nodes_from(set(candidates))
    # iterate over word-pairs, add unweighted edges into graph
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)

    for w1, w2 in pairwise(candidates):
        if w2:
            graph.add_edge(*sorted([w1, w2]))

    # score nodes using default pagerank algorithm, sort by score, keep top n_keywords
    ranks = networkx.pagerank(graph)
    if n_keywords:
        n_keywords = int(round(len(candidates) * n_keywords))
    word_ranks = {word_rank[0]: word_rank[1]
                  for word_rank in sorted(ranks.iteritems(), key=lambda x: x[1], reverse=True)[:n_keywords]}
    keywords = set(word_ranks.keys())
    # merge keywords into keyphrases
    keyphrases = {}
    j = 0
    for i, word in enumerate(words):
        if i < j:
            continue
        if word in keywords:
        	# check here the window i:i+10 !!!
            kp_words = list(takewhile(lambda x: x in keywords, words[i:i+10]))
            avg_pagerank = sum(word_ranks[w] for w in kp_words) / float(len(kp_words))
            keyphrases[' '.join(kp_words)] = avg_pagerank
            # counter as hackish way to ensure merged keyphrases are non-overlapping
            j = i + len(kp_words)
    
    return sorted(keyphrases.iteritems(), key=lambda x: x[1], reverse=True)



