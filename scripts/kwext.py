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
from nlp.tfidf import *
from nlp.stopwords import *
from conf_navigator.classes.bcolors import *
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn
from upmc_urank.models import *


def run():
	clear()
	articles = Article.objects.all()#[:200]
	extract_tfidf(articles)
	# extract_textrank()


def clear():
	print_blue('Clearing DB ...')
	PubmedKeywordStr.objects.all().delete()
	PubmedKeyphrase.objects.all().delete()
	PubmedGlobalKeyword.objects.all().delete()
	print_blue('Finished clearing DB ...')


def _lower(word):
	# Trim lower case 's' in acronyms, e.g. AEDs
	trimmed_word = word[:-1] if word[:-1].isupper() and word[-1] == 's' else word
	# Lowercase trimmed word only if it is not all uppercase
	return trimmed_word.lower() if not trimmed_word.isupper() else trimmed_word


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
					'from': i - len(word),
					'to': i
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
		# text = p 
		text = d.title + '\n' + d.abstract or ''
		filtered_chunks = extract_candidate_chunks(text)

		filtered_words = [word for phrase in filtered_chunks for word in phrase.split()]
		stemmed_words = [_stem(word) for word in filtered_words]
		tfidf.add_document(stemmed_words)

		all_stems.extend(stemmed_words)
		all_terms.extend(filtered_words) 

		term_positions[d.pk] = {
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
				'tfidf': item['tfidf'],
				'log_tfidf': item['log_tfidf'],
				'score': item['tfidf'],
				'pos_title': term_positions[d.pk]['pos_title'][stem] if stem in term_positions[d.pk]['pos_title'] else [],
				'pos_detail': term_positions[d.pk]['pos_detail'][stem] if stem in term_positions[d.pk]['pos_detail'] else [],
			}

		doc_keywords[d.pk] = kws


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


	print_blue('Time elapsed = ' +str(time.time() - tmsp))


	for i, k in enumerate(global_keywords[:100]):
		print str(i+1) + '. ' + k['term'] + ' -- score = ' + str(k['score'])
		for phrase, pos, count, stems in sorted(k['phrases'], key=lambda k:k[2], reverse=True)[:10]:
			print '\t' + phrase + ' -- ' +str(count)

	save_document_keywords(doc_keywords)
	save_global_keywords(global_keywords)
	print_blue('Total time elapsed = ' +str(time.time() - tmsp))




def save_document_keywords(doc_keywords):
	# PubmedKeywordStr.objects.all().delete()

	print_blue('Saving ' + str(len(doc_keywords)) + ' document keywords ...')
	for dpk, kws in doc_keywords.iteritems():
		keyword_obj = PubmedKeywordStr(article_id = dpk, keyword_str = json.dumps(kws))
		keyword_obj.save()

	print_blue('Finished saving document keywords')




def save_global_keywords(global_keywords):
	# PubmedGlobalKeyword.objects.all().delete()
	# PubmedKeyphrase.objects.all().delete()

	print_blue('Saving ' + str(len(global_keywords)) + ' global keywords ...')
	for gk in global_keywords:
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

	print_blue('Finished saving global keywords')


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



