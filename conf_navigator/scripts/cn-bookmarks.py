# -*- coding: utf-8 -*-

'''
SAVE BOOKMARK SEQUENCE (COMMA SEPARATED) FOR EACH USER (including old papers)
SAVE LINK user <-> talk (only new papers)

'''
import urllib2
from bs4 import BeautifulSoup as bs
from conf_navigator.models import *


def fetch_url(url):
	resp = urllib2.urlopen(url).read()
	return resp.split(',')[:-1]
	

def process_user_bookmarks(user, paper_ids):
	bookmarks = []	
	if len(paper_ids):
		bookmark = BookmarkSequence(user=user, all_bookmarks=','.join(paper_ids))
		bookmark.save()
		# User.objects.filter(pk=user.pk).update(all_bookmarks = ','.join(paper_ids))
		# user.all_bookmarks = ','.join(paper_ids)
		# user.save()
		print '** Saved ' + str(len(paper_ids)) + ' bookmarks in sequence for ' + user.name

	user.bookmarks.clear()
	# if talk is in Talk table, add link
	for pid in paper_ids:
		try:
			talk = Talk.objects.get(pk=pid)
			user.bookmarks.add(talk)
			print '\tLinked ' + user.name + ' to talk #' + str(talk.pk)
		except:
			talk = None

def run():
	url_temp = 'http://halley.exp.sis.pitt.edu/cn3/social_api_getbookmarking.php?id=[userID]'
	users = User.objects.all()
	for idx, user in enumerate(users):
		print '==== User ' + str(idx+1) + '/' + str(len(users)) +' --> ' + user.name
		url = url_temp.replace('[userID]', str(user.pk))
		paper_ids = fetch_url(url)
		process_user_bookmarks(user, paper_ids)

