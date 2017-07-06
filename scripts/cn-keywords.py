from bs4 import BeautifulSoup as bs
from conf_navigator.models import *
from nlp.keyword_extractor import *
import json

def run():
	delete_from_db()
	for event in Event.objects.all():
		print '========  ' + event.title + '  ========'
		extract_keywords(event)

	# event = Event.objects.get(pk=149)
	# extract_keywords(event)


def delete_from_db():
	TalkKeyword.objects.all().delete()
	TalkKeywordStr.objects.all().delete()
	KwPosTitle.objects.all().delete()
	KwPosAbstract.objects.all().delete()
	TalkKeyphrase.objects.all()
	ConfGlobalKeyword.objects.all().delete()


def extract_keywords(event):
	stopwords = ['research', 'professor', 'university', 'work', 'institute', 'group', 'school', 'center', 
		'program', 'webinar', 'association', 'event', 'field', 'discuss', 'editor', 'share', 'response', 'committee',
		'example', 'challenge', 'review', 'staff', 'opportunity','registration', 'effort', 'provide', 'chairman',
		'faculty', 'speaker', 'management', 'focus', 'way', 'bio', 'office', 'laboratory', 'approach', 'lecture',
		'present', 'member', 'please', 'author', 'chair', 'poster', 'level', 'fellow', 'visit', 'lunch','cover',
		'workshop', 'methodology', 'introduce', 'amount', 'answer', 'youll', 'deliver', 'chapter', 'shift',
		'attend', 'disclaimer', 'appointment', 'involvement', 'become', 'employ', 'moreover', 'definition', 
		'difficulty', 'schedule', 'attempt', 'extend', 'extension', 'scholar', 'anyone', 'everyone', 'start',
		'advisor', 'january', 'bring', 'mentor', 'deputy', 'begin', 'extent', 'consider', 'briefly',
		'highlight', 'apply', 'insight', 'taught', 'paper']



	ke = keyword_extractor({
		'abstract_weight' : 0.8,
		'stopwords': stopwords,
		'min_rep_global_keyword': 3
	})

	talks = Talk.objects.filter(event=event)
	for t in talks:
		doc = {
			'id': t.pk,
			'title' : t.title,
			'abstract': t.abstract,
		}		
		ke.add_document(doc)

	ke.extract()

	""" SAVE DOCUMENT KEYWORDS """
	n = len(talks)
	for i, talk in enumerate(talks):
		doc_keywords = {}
		for stem, k in ke.get_document_keywords(i).iteritems():
			pos_title = k['pos_title'] or []
			pos_title_str = json.dumps(pos_title)
			pos_detail = k['pos_abstract'] or []
			pos_detail_str =  json.dumps(pos_detail)

			# Save doc keywords as proper entries in DB
			talk_kw = TalkKeyword(stem=stem, tfidf=k['tfidf'], tf=k['tf'], score=k['score'], is_title=k['is_title'], pos_title=pos_title_str, pos_detail=pos_detail_str, talk=talk)
			talk_kw.save()
			# Save positions of keyword in title
			if k['pos_title'] is not None:
				for pos in k['pos_title']:
					kpt = KwPosTitle(from_pos=pos['from'], to_pos=pos['to'], talk_kw=talk_kw)
					kpt.save()
			# Save positions of keyword in detail
			if k['pos_abstract'] is not None:
				for pos in k['pos_abstract']:
					kpa = KwPosAbstract(from_pos=pos['from'], to_pos=pos['to'], talk_kw=talk_kw)
					kpa.save()

			# Save doc keywords as strings
			doc_keywords[stem] = {
				'stem' : stem,
				'tfidf' : k['tfidf'], 
				'tf' : k['tf'], 
				'score' : k['score'], 
				'pos_title' : pos_title,
				'pos_detail' : pos_detail
			}

		keywords_str = TalkKeywordStr(keyword_str=json.dumps(doc_keywords), talk=talk)
		keywords_str.save()
		print 'Saved keywords for talk = ' + str(talk.pk) + ' (' + str(i+1) + '/' + str(n) +')'

	""" SAVE GLOBAL KEYWORDS """
	global_keywords = ke.get_global_keywords()
	keyphrases, stem_to_phrases = ke.get_keyphrases()
	print 'Global keywords = ' + str(len(global_keywords))

	# Save keyphrases and keep model objects in dict_phrase
	dict_phrase = {}
	for kp in keyphrases:
		keyphrase = TalkKeyphrase(phrase=kp['phrase'], sequence=json.dumps(kp['sequence']), count=kp['count'])
		keyphrase.save(using="confnavdb")
		print 'Saved keyphrase = ' + kp['phrase']
		dict_phrase[kp['phrase']] = keyphrase

	n = len(global_keywords)
	for i, gk in enumerate(global_keywords):
		stem = gk['stem']
		variations_str = ' '.join([v['term'] for v in gk['variations']])
		num_keyphrases = len(stem_to_phrases[stem]) if stem in stem_to_phrases else 0
		global_kw =  ConfGlobalKeyword(
			stem=stem, 
			term=gk['term'], 
			df=gk['df'], entropy=gk['entropy'], 
			score=gk['score'], 
			variations=variations_str, 
			num_keyphrases=num_keyphrases,
			event = event
		)
		global_kw.save(using="confnavdb")
		print '('+ str(i+1) + '/' + str(n) +') Saved global keyword --> stem "'+stem+'", term ="'+ str(global_kw.term) + '" , df = ' + str(global_kw.df) + ', ent = ' + str(global_kw.entropy)


		if stem in stem_to_phrases:
			# print '\tAdding links "' + stem +'" <--> " keyphrases'
			for phrase in stem_to_phrases[stem]:
				if phrase in dict_phrase:
					keyphrase = dict_phrase[phrase]
					global_kw.talk_keyphrases.db_manager('confnavdb').add(keyphrase)
					# print '\t'+ str(i+1) + '/' + str(n) +' Link  "' + gk['stem'] +'" <--> "' + phrase + '" ('+str(gk['df']) +')'
