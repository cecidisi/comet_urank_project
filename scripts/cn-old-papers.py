# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2
import json
import unicodedata
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit
from conf_navigator.models import *
from nlp.keyword_extractor import *
from nlp.stopwords import *
from django.core.exceptions import ObjectDoesNotExist


def clear_db():
	OldPaper.objects.all().delete()



def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')


def fetch_paper(contentID):
	url_temp = "http://halley.exp.sis.pitt.edu/cn3/social_api_getcontents.php?cid=[contentID]"
	url = url_temp.replace('[contentID]', str(contentID))
	resp = urllib2.urlopen(url).read()
	soup = bs(resp, 'lxml')
	if soup.find('title') and soup.find('title').get_text() != '':
		title = ''
		try:
			title = clean_text(soup.find('title').get_text())
		except Exception, e:
			print str(e)
			print soup.find('title').get_text()

		abstract = ''
		try:
			abstract = clean_text(soup.find('abstract').get_text())
		except Exception, e:
			print str(e) 
			print soup.find('abstract').get_text()

		return {
			'id': contentID,
			'title': title,
			'abstract': abstract,
			'authorids': soup.find('authorids').get_text()[:-1] #.split(',')[:-1]
		}
	return None


def find_old_papers():
	old_papers = {}
	old_papers_in_db = {}
	talks = {}

	for op in OldPaper.objects.all():
		old_papers_in_db[str(op.pk)] = True

	for talk in Talk.objects.all():
		talks[str(talk.pk)] = True

	def is_talk(contentID):
		return True if contentID in talks else False

	def is_old_paper(contentID):
		if contentID in old_papers or contentID in old_papers_in_db:
			return True
		return False

	bookmark_sequences = BookmarkSequence.objects.all() #[2:5]
	print str(len(bookmark_sequences)) + ' bookmark sequences'
	for seq in bookmark_sequences:
		all_bookmarks = seq.all_bookmarks.split(',')
		print str(len(all_bookmarks)) + ' ids in all bookmarks for user ' + str(seq.user.id)
		for idx, contentID in enumerate(all_bookmarks):
			step = '(' + str(idx+1) + '/' + str(len(all_bookmarks)) + ')'
			if not is_talk(contentID) and not is_old_paper(contentID):
				op = fetch_paper(contentID)
				if op:
					old_papers[contentID] = op
					print '=== ' + step + ' Found old paper #' + str(contentID)
				else:
					print 'xxx ' + step + ' No paper found for contentID = ' + str(contentID)
			else:
				print '*** ' + step + ' Paper #' + str(contentID) + ' already exists'
	return [op for op in old_papers.values()]



def save_and_extact_keywords(old_papers):
	ke = keyword_extractor({ 'stopwords': stopwords, 'doc_keywords_only': True })
	for op in old_papers:
		ke.add_document(op)

	ke.extract()
	for idx, op in enumerate(old_papers):
		doc_keywords = ke.get_document_keywords(idx)
		try:
			old_paper = OldPaper.objects.create(
				id = op['id'], 
				title = op['title'] if op['title'] else '', 
				abstract = op['abstract'] if op['abstract'] else '', 
				authorids = op['authorids'],
				keyword_str = json.dumps(doc_keywords) 
			)
			print 'Saved old paper #' +str(old_paper.id)+ ' (with '+ str(len(doc_keywords)) +' keywords)'
		except Exception, e:
			print str(e)
			print op['title']
			print op['abstract']


				

def run():	
	# clear_db()
	old_papers = find_old_papers()
	print 'Fetched ' + str(len(old_papers)) + ' old papers'
	save_and_extact_keywords(old_papers)

