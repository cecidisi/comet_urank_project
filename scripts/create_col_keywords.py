import json
from nlp.keyword_extractor import *
from comet_urank.models import *

def extract_col_keywords():
	KeywordPosTitle.objects.all().delete()
	KeywordPosDetail.objects.all().delete()
	ColKeyword.objects.all().delete()
	ColKeywordStr.objects.all().delete()
	Keyphrase.objects.all().delete()
	GlobalKeyword.objects.all().delete()

	stopwords = ['research', 'professor', 'university', 'work', 'institute', 'group', 'school', 'center', 
		'program', 'webinar', 'association', 'event', 'field', 'discuss', 'editor', 'share', 'response', 'committee',
		'example', 'challenge', 'review', 'staff', 'opportunity','registration', 'effort', 'provide', 'chairman',
		'faculty', 'speaker', 'management', 'focus', 'way', 'bio', 'office', 'laboratory', 'approach', 'lecture',
		'present', 'member', 'please', 'author', 'chair', 'poster', 'level', 'fellow', 'visit', 'lunch','cover',
		'workshop', 'methodology', 'introduce', 'amount', 'answer', 'youll', 'deliver', 'chapter', 'shift',
		'attend', 'disclaimer', 'appointment', 'involvement', 'become', 'employ', 'moreover', 'definition', 
		'difficulty', 'schedule', 'attempt', 'extend', 'extension', 'scholar', 'anyone', 'everyone', 'start',
		'advisor', 'january', 'bring', 'mentor', 'deputy', 'begin', 'extent', 'consider', 'briefly',
		'highlight', 'apply', 'insight', 'taught']

	colvideos = Colvideo.objects.all() #[:100]
	n = len(colvideos)
	ke = keyword_extractor({
		'stopwords': stopwords,
		'min_rep_global_keyword': 3
	})
	for cv in colvideos:
		doc = {
			'id': cv.pk,
			'title' : cv.title,
			'abstract': cv.detail,
		}
		ke.add_document(doc)

	ke.extract()

	# for i, c in enumerate(colvideos):
	# 	print '*************  '+c.title
	# 	for stem, k in ke.get_document_keywords(i).iteritems():
	# 		print stem
	# 		obj = dict(k)
	# 		del obj['pos_title']
	# 		del obj['pos_abstract']
	# 		print obj

	
	""" SAVE DOCUMENT KEYWORDS """
	for i, cv in enumerate(colvideos):
		doc_keywords = {}
		for stem, k in ke.get_document_keywords(i).iteritems():
			pos_title = k['pos_title'] or []
			pos_title_str = json.dumps(pos_title)
			pos_detail = k['pos_abstract'] or []
			pos_detail_str =  json.dumps(pos_detail)

			# Save doc keywords as proper entries in DB
			col_kw = ColKeyword(stem=stem, tfidf=k['tfidf'], tf=k['tf'], score=k['score'], is_title=k['is_title'], pos_title=pos_title_str, pos_detail=pos_detail_str, colvideo=cv)
			col_kw.save()
			# Save positions of keyword in title
			if k['pos_title'] is not None:
				for pos in k['pos_title']:
					kpt = KeywordPosTitle(from_pos=pos['from'], to_pos=pos['to'], col_kw=col_kw)
					kpt.save()
			# Save positions of keyword in detail
			if k['pos_abstract'] is not None:
				for pos in k['pos_abstract']:
					kpd = KeywordPosDetail(from_pos=pos['from'], to_pos=pos['to'], col_kw=col_kw)
					kpd.save()

			# Save doc keywords as strings
			doc_keywords[stem] = {
				'stem' : stem,
				'tfidf' : k['tfidf'], 
				'tf' : k['tf'], 
				'score' : k['score'], 
				# 'is_title' : k['is_title'], 
				'pos_title' : pos_title,
				'pos_detail' : pos_detail
			}
		keywords_str = ColKeywordStr(keyword_str=json.dumps(doc_keywords), colvideo=cv)
		keywords_str.save()
		# print '\tSaved '+str(len(doc_keywords))+' keywords into keywords_str "' + str(keywords_str.pk) + '" for colvideo = ' + str(cv.pk)

		print 'Saved keywords for colvideo = ' + str(cv.pk) + ' (' + str(i+1) + '/' + str(n) +')'


	""" SAVE GLOBAL KEYWORDS """
	global_keywords = ke.get_global_keywords()
	keyphrases, stem_to_phrases = ke.get_keyphrases()
	print 'Global keywords = ' + str(len(global_keywords))

	# Save keyphrases and keep model objects in dict_phrase
	dict_phrase = {}
	for kp in keyphrases:
		keyphrase = Keyphrase(phrase=kp['phrase'], sequence=json.dumps(kp['sequence']), count=kp['count'])
		keyphrase.save()
		print 'Saved keyphrase = ' + kp['phrase']
		dict_phrase[kp['phrase']] = keyphrase

	n = len(global_keywords)
	for i, gk in enumerate(global_keywords):
		stem = gk['stem']
		variations_str = ' '.join([v['term'] for v in gk['variations']])
		num_keyphrases = len(stem_to_phrases[stem]) if stem in stem_to_phrases else 0
		global_kw =  GlobalKeyword(stem=stem, term=gk['term'], df=gk['df'], entropy=gk['entropy'], score=gk['score'], variations=variations_str, num_keyphrases=num_keyphrases)
		global_kw.save()
		print '('+ str(i+1) + '/' + str(n) +') Saved global keyword --> stem "'+stem+'", term ="'+ str(global_kw.term) + '" , df = ' + str(global_kw.df) + ', ent = ' + str(global_kw.entropy)


		# print '\tAdding links "'+ stem +'" <--> colvideos'
		for cv_id in gk['appears_in']:
			cv = Colvideo.objects.get(pk=cv_id)
			global_kw.colvideos.add(cv)

		if stem in stem_to_phrases:
			# print '\tAdding links "' + stem +'" <--> " keyphrases'
			for phrase in stem_to_phrases[stem]:
				if phrase in dict_phrase:
					keyphrase = dict_phrase[phrase]
					global_kw.keyphrases.add(keyphrase)
					# print '\t'+ str(i+1) + '/' + str(n) +' Link  "' + gk['stem'] +'" <--> "' + phrase + '" ('+str(gk['df']) +')'


def run():
	extract_col_keywords()




