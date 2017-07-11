# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2
import math
import json
import csv
import unicodedata
from bs4 import BeautifulSoup as bs
import numpy as np
from conf_navigator.models import *
from nlp.matrix_factorization import *
from nlp.keyword_extractor import *
from nlp.stopwords import *
from django.core.exceptions import ObjectDoesNotExist


def clear_db():
	SimUserNeighbor.objects.all().delete()


def get_participants(eventID):
	participants = User.objects.filter(events__pk=eventID)
	return participants


def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')



def get_similar_users(cid, uid, friends):
	url_temp = "http://halley.exp.sis.pitt.edu/cn3/social_api_getrelevance.php?cid=[cid]&uid=[uid]"
	url = url_temp.replace('[cid]', str(cid)).replace('[uid]', str(uid))
	soup = bs(urllib2.urlopen(url).read(), 'lxml')
	text = clean_text(soup.find('body').get_text())
	rows = text.split('\n')
	header = rows[0].split(',')
	scores = ['P', 'C', 'I', 'G', 'S']
	neighbors = []
	for row in rows[1:]:
		obj = {}
		# process individual values in csv row
		for i, attr in enumerate(row.split(',')):
			obj['score'] = 0.0
			# add PCIGS sub-scores
			if header[i] in scores:
				sub_score = float(attr) if attr != '' else 0.0
				obj[header[i]] = sub_score
				obj['score'] += sub_score
			elif header[i] == 'AuthorID' or header[i] == 'UserID':
				obj[header[i]] = int(attr) if attr != '' else None
			else: # Name
				obj[header[i]] = attr
		# check at the end if the neighbor is friends with current user
		neighborID = obj['UserID'] if 'UserID' in obj else None
		obj['friend'] = 1.0 if neighborID in friends else 0.0
		obj['score'] += obj['friend']
		neighbors.append(obj)
	return neighbors



def get_neighbor_or_create(v):
	# neighbor = None
	# Try to find neighbor by ID
	if v['UserID']:
		try:
			# user already registered with original ID
			neighbor = User.objects.get(pk=v['UserID'])
			return neighbor
		except:
			neighbor = None
	# Try to find neighbor by name
	try:
		# neighbor could be already saved as 'added' in cn-talks bc was found as author. Change id and type
		v_id = v['UserID'] if v['UserID'] else User.objects.all().order_by('-id')[0].id + 1
		neighbor = User.objects.get(name=v['Name'])
		neighbor.id = v_id
		neighbor.type = 'original'
		neighbor.save()
		print '** Change user type, new id = ' + str(neighbor.pk) # + ' (matches ' + str(v['UserID']) + ')'
		return neighbor
	except:
		# Neighbor doesn't exist, create user with type = 'added'
		try:
			new_id = User.objects.all().order_by('-id')[0].id + 1
			neighbor = User.objects.create(
				id = new_id,
				name = v['Name'],
				username = v['Name'].replace(' ', '_'),
				type = 'added'
			)
			print '++ Added new user -> ' + neighbor.name
			return neighbor
		except:
			# should not be here
			print 'Fetched user'
			print v
			print 'User in DB'
			user  = User.objects.get(pk=new_id)
			print user.name + ', id = '+ str(user.pk)
			return None



def save_sim_user_neighbor(event, user, neighbors):	
	count_v = 0
	for v in neighbors:
		if v['score']:
			neighbor = get_neighbor_or_create(v)
			if neighbor:
				prev_sims = SimUserNeighbor.objects.filter(user=user).filter(neighbor=neighbor)
				if len(prev_sims) == 0:
					sim_u_v = SimUserNeighbor(user=user, neighbor=neighbor, score=v['score'],
						pub_sim = v['P'], co_auth = v['C'], interest = v['I'], geo_dist= v['G'],
						soc_ctx = v['S'], friend = v['friend'], event = event)
					sim_u_v.save()
					count_v += 1
	print '=== SAVED ' + str(count_v )+ ' neighbors for '+ user.name



def run():
	clear_db()
	event_ids = [149]
	print 'CALCULATE USER-NEIGHBOR SIMILARITY'
	for eventID in event_ids:		
		event = Event.objects.get(pk=eventID)
		print '\nEvent #' + str(eventID) + ' --> ' + event.title
		participants = get_participants(eventID) #[:3]
		print 'Participants for ' + event.title + ' = ' + str(len(participants))
		for i, user in enumerate(participants):
			step = '(' + str(i+1) + '/' + str(len(participants)) + ')'
			print '\n' + step + ' ==> #' + str(user.pk) + ' - ' + user.name
			friends = get_friends(user.pk)
			neighbors = get_similar_users(event.pk, user.pk, friends)
			save_sim_user_neighbor(event, user, neighbors)


def get_friends(user_id):
	temp_url = "http://halley.exp.sis.pitt.edu/cn3mobile/friendlist.jsp?userID=[userID]"
	url = temp_url.replace('[userID]', str(user_id))
	soup = bs(urllib2.urlopen(url).read(), 'xml')
	# friends of current user
	friends = {}
	for f in soup.find_all('Item'):
		userID =  int(f.find('userID').get_text())
		friends[userID] = True
	return friends
	














