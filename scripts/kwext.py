from functools import reduce
import collections
from collections import Counter
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

from upmc_urank.models import *


def run():

	pmids = [28212466]
	# articles = Article.objects.filter(pk__in = pmids)
	articles = ["WITHDRAWN: Propranolol for migraine prophylaxis.\nBACKGROUND: Propranolol is one of the most commonly prescribed drugs for migraine prophylaxis. OBJECTIVES: We aimed to determine whether there is evidence that propranolol is more effective than placebo and as effective as other drugs for the interval (prophylactic) treatment of patients with migraine. SEARCH METHODS: Potentially eligible studies were identified by searching MEDLINE/PubMed (1966 to May 2003) and the Cochrane Central Register of Controlled Trials (Issue 2, 2003), and by screening bibliographies of reviews and identified articles. SELECTION CRITERIA: We included randomised and quasi-randomised clinical trials of at least 4 weeks duration comparing clinical effects of propranolol with placebo or another drug in adult migraine sufferers. DATA COLLECTION AND ANALYSIS: Two reviewers extracted information on patients, methods, interventions, outcomes measured, and results using a pre-tested form. Study quality was assessed using two checklists (Jadad scale and Delphi list). Due to the heterogeneity of outcome measures and insufficient reporting of the data, only selective quantitative meta-analyses were performed. As far as possible, effect size estimates were calculated for single trials. In addition, results were summarised descriptively and by a vote count among the reviewers. MAIN RESULTS: A total of 58 trials with 5072 participants met the inclusion criteria. The 58 selected trials included 26 comparisons with placebo and 47 comparisons with other drugs. The methodological quality of the majority of trials was unsatisfactory. The principal shortcomings were high dropout rates and insufficient reporting and handling of this problem in the analysis. Overall, the 26 placebo-controlled trials showed clear short-term effects of propranolol over placebo. Due to the lack of studies with long-term follow up, it is unclear whether these effects are stable after stopping propranolol. The 47 comparisons with calcium antagonists, other beta-blockers, and a variety of other drugs did not yield any clear-cut differences. Sample size was, however, insufficient in most trials to establish equivalence. AUTHORS' CONCLUSIONS: Although many trials have relevant methodological shortcomings, there is clear evidence that propranolol is more effective than placebo in the short-term interval treatment of migraine. Evidence on long-term effects is lacking. Propranolol seems to be as effective and safe as a variety of other drugs used for migraine prophylaxis."]
	
	for p in articles:

		text = p #p.title + '\n' + p.abstract
		candidate_chunks = extract_candidate_chunks(text)
		candidate_words = extract_candidate_words(text)

		print_blue('Candidate Chunks')
		print candidate_chunks
		print_blue('Candidate Words')
		print candidate_words





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

	
	# key = returned inlambda function: T or F
	candidates = [' '.join(word for word, pos, chunk in group).lower() 
		for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]
	# print '==== CANDIDATES ===='
	# print candidates

	filtered = [cand for cand in candidates 
		if cand not in stopwords 
		and not all(char in punct for char in cand) 
		# and all(word not in stopwords for word in cand.split(' '))
		# and len(cand.split(' ')) <= 3
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







