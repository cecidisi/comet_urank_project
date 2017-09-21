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
from nlp.tfidf import *
from nlp.stopwords import *
from conf_navigator.classes.bcolors import *
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn


from upmc_urank.models import *

stopwords = ['questionnaire', 'presence', 'insights', 'characteristics', 'aspect', 'position', 
'interpretation', 'differences', 'analysis']

def run():
	extract_tfidf()
	# extract_textrank()



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






def extract_tfidf():
	wnl = nltk.WordNetLemmatizer()
	stemmer = nltk.PorterStemmer()
	tfidf = TfIdf() # own
	
	articles = Article.objects.all()[:100]
	tmsp = time.time()

	all_documents = []
	doc_keywords = {}
	# tfidf_all dictionary of single words. stem: { tfidf_sum, count }
	tfidf_all = {}
	phrase_count = {}
	for i, p in enumerate(articles):

		print 'Article #' + str(i+1) + '/' + str(len(articles)) + '\n'
		# text = p 
		text = p.title + '\n' + p.abstract or ''
		filtered_chunks = extract_candidate_chunks(text)

		filtered_words = [word for phrase in filtered_chunks for word in phrase.split()]
		stemmed_words = [stemmer.stem(wnl.lemmatize(word)) for word in filtered_words]

		# print text
		# print_blue('N Grams')
		# print filtered_chunks
		# print_blue('Candidate Words')
		# print filtered_words

		tfidf.add_document(stemmed_words)

		# collection key phrases
		for k in filtered_chunks:
			phrase_count[k] = 1 if not k in phrase_count else phrase_count[k] + 1


	# sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True)
	# representation = sklearn_tfidf.fit_transform(all_documents)
	# print representation


	# document single-term keywords
	for idx, d in enumerate(articles):
		kws = {}
		for item in tfidf.list_terms(idx):
			# document term
			stem = item['term']
			log_tfidf = log(item['tfidf'])
			kws[stem] = {
				'tfidf': item['tfidf'],
				'log_tfidf': item['log_tfidf'],
				'score': log_tfidf
			}

			# update global tfidf list
			if stem not in tfidf_all:
				tfidf_all[stem] = {
					'count': 0,
					'tfidf_sum': 0
				}
			tfidf_all[stem]['count'] += 1
			tfidf_all[stem]['tfidf_sum'] += item['tfidf']

		doc_keywords[d.pk] = kws



	# collection key phrases from chunks
	term_info = tfidf.get_term_info()

	term_phrases = {}
	keyphrases = []
	for phrase, count in phrase_count.iteritems():
		obj = {
			'score': 0,
			'stems': [],
			'term': phrase,
			'count': count
		}
		terms = phrase.split()
		for term in terms:
			stem = stemmer.stem(wnl.lemmatize(term))
			if stem in tfidf_all and stem in term_info:
				# obj['score'] += tfidf_all[stem]['tfidf_sum'] / float(tfidf_all[stem]['count'])
				obj['score'] += term_info[stem]['df']
				obj['stems'].append(stem)
			obj['score'] /= float(len(terms))

			# freq terms on key phrases
			if stem not in term_phrases:
				term_phrases[stem] = {
					'count': 0,
					'phrases': {}
				}
			if phrase not in term_phrases[stem]:
				term_phrases[stem]['phrases'][phrase] = 0
			term_phrases[stem]['count'] += 1
			term_phrases[stem]['phrases'][phrase] += 1


		keyphrases.append(obj)


	# keyphrases = sorted(keyphrases, key=lambda k: k['score'], reverse=True)


	global_terms = sorted([(term, value) for term, value in term_phrases.iteritems()], key=lambda k: k[1]['count'], reverse=True)


	print_blue('time elapsed = ' +str(time.time() - tmsp))


	for i, k in enumerate(global_terms[:50]):
		print str(i+1) + '. ' + k[0] + ' -- ' + str(k[1]['count'])
		print '\n\t'.join(k[1]['phrases'].keys()[:20])



	# for i in range(0, 100):
	# 	k = keyphrases[i]
	# 	print str(i+1) + '. ' + k['term'] + ' -- ' + str(k['count']) + ' -- ' +  str(round(k['score'], 4))



	# tmp = sorted([(word, item['tfidf_sum']) for word, item in tfidf_all.iteritems()], 
	# 	key= lambda k: k[1], reverse=True)
	# for i, item in enumerate(tmp[:100]):
	# 	print str(i+1) + '. ' + item[0] + ' -- ' + str(round(item[1], 4))


	# global_terms = sorted([value for value in term_info.values()], key = lambda k: k['df'], reverse = True)
	# for i, k in enumerate(global_terms[:100]):
	# 	try:
	# 		print str(i+1) + '. ' + k['term'] + ', df = ' + str(k['df']) + ', comm = ' + str(k['commonness'])
	# 	except:
	# 		print k['term']





def save_document_keywords(doc_keywords):

	for pid, kws in doc_keywords:
		# article = Article.objects.get(pk = pid)
		keyword_obj =  PubmedKeywordStr(article_id = pid, keyword_str = json.dumps(kws))
		keyword_obj.save()

	print_blue('Finished saving document keywords')





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
	# print '==== TAGGED SENTENCES ===='
	# print tagged_sents

	all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
		for tagged_sent in tagged_sents))
	# print '==== ALL CHUNKS ====	'
	# print all_chunks
	
	# key = returned in lambda function: T or F
	candidates = [' '.join(word for word, pos, chunk in group).lower() 
		for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]
	# print '==== CANDIDATES ===='
	# print candidates

	filtered = [cand for cand in candidates 
		if cand not in stopwords 
		and not all(char in punct for char in cand) 
		and len(cand.split()) > 1
		and len(cand) > 4
		# and all(len(term) > 3 and term not in punt and not is_number(term) for term in cand)
		]

	# print '==== FILTERED ===='
	# print filtered
	return filtered



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




