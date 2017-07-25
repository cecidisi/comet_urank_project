# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup as bs
import json
from nlp.keyword_extractor import *
from upmc_urank.models import *


def delete_from_db():
	PubmedKeyphrase.objects.all().delete()
	PubmedGlobalKeyword.objects.all().delete()
	PubmedKeywordStr.objects.all().delete()


def run():
	delete_from_db()
	articles = Article.objects.all()
	extract_keywords(articles)



def extract_keywords(articles):

	ke = keyword_extractor({
		'abstract_weight' : 0.8,
		'min_rep_global_keyword': 5
	})

	for d in articles:
		doc = {
			'id': d.pk,
			'title' : d.title,
			'abstract': d.abstract,
		}		
		ke.add_document(doc)
	ke.extract()

	""" SAVE DOCUMENT KEYWORDS """
	n = len(articles)
	for i, d in enumerate(articles):
		doc_keywords = {}
		for stem, k in ke.get_document_keywords(i).iteritems():
			pos_title = k['pos_title'] or []
			# pos_title_str = json.dumps(pos_title)
			pos_detail = k['pos_abstract'] or []
			# pos_detail_str =  json.dumps(pos_detail)

			# # Save doc keywords as proper entries in DB
			# talk_kw = TalkKeyword(stem=stem, tfidf=k['tfidf'], tf=k['tf'], score=k['score'], is_title=k['is_title'], pos_title=pos_title_str, pos_detail=pos_detail_str, talk=talk)
			# talk_kw.save()
			# # Save positions of keyword in title
			# if k['pos_title'] is not None:
			# 	for pos in k['pos_title']:
			# 		kpt = KwPosTitle(from_pos=pos['from'], to_pos=pos['to'], talk_kw=talk_kw)
			# 		kpt.save()
			# # Save positions of keyword in detail
			# if k['pos_abstract'] is not None:
			# 	for pos in k['pos_abstract']:
			# 		kpa = KwPosAbstract(from_pos=pos['from'], to_pos=pos['to'], talk_kw=talk_kw)
			# 		kpa.save()

			# Save doc keywords as strings
			doc_keywords[stem] = {
				'stem' : stem,
				'tfidf' : k['tfidf'], 
				'tf' : k['tf'], 
				'score' : k['score'], 
				'pos_title' : pos_title,
				'pos_detail' : pos_detail
			}

		keywords_str = PubmedKeywordStr(keyword_str=json.dumps(doc_keywords), article=d)
		keywords_str.save()
		print 'Saved keywords for article = ' + str(d.pk) + ' (' + str(i+1) + '/' + str(n) +')'

	""" SAVE GLOBAL KEYWORDS """
	global_keywords = ke.get_global_keywords()
	keyphrases, stem_to_phrases = ke.get_keyphrases()
	print 'Global keywords = ' + str(len(global_keywords))

	# Save keyphrases and keep model objects in dict_phrase
	dict_phrase = {}
	for kp in keyphrases:
		keyphrase = PubmedKeyphrase(phrase=kp['phrase'], sequence=json.dumps(kp['sequence']), count=kp['count'])
		keyphrase.save(using="upmcdb")
		print 'Saved keyphrase = ' + kp['phrase']
		dict_phrase[kp['phrase']] = keyphrase

	n = len(global_keywords)
	for i, gk in enumerate(global_keywords):
		stem = gk['stem']
		variations_str = ' '.join([v['term'] for v in gk['variations']])
		num_keyphrases = len(stem_to_phrases[stem]) if stem in stem_to_phrases else 0
		global_kw = PubmedGlobalKeyword(
			stem=stem, 
			term=gk['term'], 
			df=gk['df'], entropy=gk['entropy'], 
			score=gk['score'], 
			variations=variations_str, 
			num_keyphrases=num_keyphrases
		)
		global_kw.save(using="upmcdb")
		try:
			print '('+ str(i+1) + '/' + str(n) +') Saved global keyword --> stem "'+str(stem)+'", term ="'+ str(global_kw.term) + '" , df = ' + str(global_kw.df) + ', ent = ' + str(global_kw.entropy)
		except Exception, e:
			# print_red(str(e))
			print stem			

		if stem in stem_to_phrases:
			# print '\tAdding links "' + stem +'" <--> " keyphrases'
			for phrase in stem_to_phrases[stem]:
				if phrase in dict_phrase:
					keyphrase = dict_phrase[phrase]
					global_kw.keyphrases.db_manager('upmcdb').add(keyphrase)
					# print '\t'+ str(i+1) + '/' + str(n) +' Link  "' + gk['stem'] +'" <--> "' + phrase + '" ('+str(gk['df']) +')'


