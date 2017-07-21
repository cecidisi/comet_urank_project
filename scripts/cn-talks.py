# -*- coding: utf-8 -*-

'''
READ SESSIONS AND PAPERS
'''

from __future__ import unicode_literals
import sys
import os
from django.core.exceptions import ObjectDoesNotExist
import urllib2
from bs4 import BeautifulSoup as bs
from bs4 import UnicodeDammit
from conf_navigator.models import *
from conf_navigator.classes.bcolors import *
import datetime
import json
import unicodedata


def get_date(date):
	try:
		return datetime.datetime.strptime(date, "%m-%d-%Y")
	except Exception, e:
		print str(e)
		return None


def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')


def process_papers(papers):
	eventId = papers[0].find('eventID').get_text()
	event = Event.objects.get(pk=eventId)

	for idx, item in enumerate(papers):
		
		# Save event session if not exist
		session, created = Session.objects.get_or_create(
			id = item.find('eventSessionID').get_text(),
			name = item.find('sessionName').get_text(),
			date = get_date(item.find('sessionDate').get_text()) if item.find('sessionDate') else None,
			start_time = item.find('sessionStartTime').get_text() if item.find('sessionStartTime') else None,
			end_time = item.find('sessionEndTime').get_text() if item.find('sessionEndTime') else None,
			location = item.find('location').get_text() if item.find('location') else None,
			event = event
		)
		if created:
			print '=== Created Session #' + str(session.pk) + ' -> ' + session.name

		content_type = item.find('contentType').get_text()
		title = clean_text(item.find('paperTitle').get_text())
		abstract = clean_text(item.find('paperAbstract').get_text())
		
		if content_type != 'no-paper':
			try:
				talk = Talk.objects.create(
					id = item.find('contentID').get_text(),
					title =  title,
					abstract = abstract,
					content_type = item.find('contentType').get_text(),
					author_list = item.find('authors').get_text() if item.find('authors') else '', 
					address = item.find('address').get_text() if item.find('address') else '',
					presentation_id = item.find('presentationID').get_text() if item.find('presentationID') else None,
					date = get_date(item.find('paperDate').get_text()) if item.find('paperDate') else None,
					begin_time = item.find('begintime').get_text() if item.find('begintime') else None,
					end_time = item.find('endtime').get_text() if item.find('endtime') else None,
					event = event,
					session = session
				)
				print '* Saved talk #'+ str(talk.pk)+' --> ' + talk.title
			except Exception, e:
				print_red(str(session.pk))
				print_red(str(e))

			# Link talk to each author. If author not exist, create w/ type = 'added'
			# talk.authors.clear()
			for author_name in talk.author_list.split(','):
				if author_name != '':
					user = None
					try:
						user = User.objects.get(name=author_name)
					except:
						# Get highest ID + 1 (Assumes users are already loaded in DB)
						new_id = User.objects.all().order_by('-id')[0].id + 1
						user = User.objects.create(
							id = new_id,
							name = author_name,
							username = author_name.replace(' ', '_'),
							type = 'added'
						)
						print '\t Added user ' + user.name
					print user
					# Fails if author is repeated, e.g. Flavio Nazareno
					try:	
						user.talks.add(talk)
						print '\t Linked talk to author -> ' + user.name
					except:
						print '\t Author -> ' + user.name + ' already linked'

		else:
			print 'Not saving "no-paper" '+ title


def fetch_url(url):
	# resp = urllib2.urlopen(url).read().decode("windows-1252").encode("utf8")
	resp = urllib2.urlopen(url).read()
	soup = bs(resp, 'xml')
	return soup


def delete_from_db():
	Talk.objects.all().delete()
	Session.objects.all().delete()


def run():
	url = 'http://halley.exp.sis.pitt.edu/cn3mobile/allSessionsAndPapers.jsp?conferenceID='
	conf_ids = [149]
	delete_from_db()
	for conf_id in conf_ids:
		papers = fetch_url(url + str(conf_id)).find_all('Item')
		process_papers(papers)




