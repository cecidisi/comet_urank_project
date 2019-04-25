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


def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')



def get_participants(eventID):
	participants = User.objects.filter(events__pk=eventID)
	return participants



def get_new_papers(talks):
	new_papers = {}
	# Fetch papers in DB (future items)
	for p in talks:
		paper = {
			'id': p.pk,
			'title': p.title, 
			'abstract': p.abstract,
			'authorids': p.author_list.split(','),
			'keywords': {}
		}
		for k in p.talk_keywords.all():
			paper['keywords'][k.stem] = { 'tf': k.tf}
		new_papers[p.pk] = paper
		# print 'Added new paper #' + str(paper['id']) + ' -- ' + paper['title']
	return new_papers



def get_old_papers():
	print 'FETCH OLD PAPERS'
	old_papers = {}
	for op in OldPaper.objects.all():
		author_list = [int(author) for author in op.authorids.split(',')] if op.authorids else []
		old_paper = {
			'id': op.pk,
			'title': op.title, 
			'abstract': op.abstract,
			'authorids': author_list,
			'keywords': json.loads(op.keyword_str)
		}
		old_papers[op.pk] = old_paper
	return old_papers



def get_friends(user_id):
	temp_url = "http://halley.exp.sis.pitt.edu/cn3mobile/friendlist.jsp?userID=[userID]"
	url = temp_url.replace('[userID]', str(user_id))
	resp = urllib2.urlopen(url).read()
	soup = bs(resp, 'xml')
	# friends of current user
	friends = {}
	for f in soup.find_all('Item'):
		userID =  int(f.find('userID').get_text())
		friends[userID] = True
	return friends



def get_social_neighbors(cid, uid, friends):
	url_temp = "http://halley.exp.sis.pitt.edu/cn3/social_api_getrelevance.php?cid=[cid]&uid=[uid]"
	url = url_temp.replace('[cid]', str(cid)).replace('[uid]', str(uid))
	resp = urllib2.urlopen(url).read()
	soup = bs(resp, 'lxml')
	text = clean_text(soup.find('body').get_text())
	rows = text.split('\n')
	header = rows[0].split(',')
	scores = ['P', 'C', 'I', 'G', 'S']
	# neighbors = []
	neighbors = {}

	for row in rows[1:]:
		obj = { 'score': 0.0, 'details': {} }
		# process individual values in csv row
		for i, attr in enumerate(row.split(',')):
			# add PCIGS sub-scores
			if header[i] in scores:
				feature_name = header[i]
				sub_score = float(attr) if attr != '' else 0.0
				obj[feature_name] = sub_score
				obj['score'] += sub_score
				obj['details'][feature_name] = sub_score
				# handle UserID and AuthorID
			elif header[i] == 'AuthorID' or header[i] == 'UserID':
				obj[header[i]] = int(attr) if attr != '' else None
			else: # Name
				obj[header[i]] = attr
		# check at the end if the neighbor is friends with current user
		neighborID = obj['UserID'] if 'UserID' in obj else None
		friend_score = 1.0 if neighborID in friends else 0.0
		obj['friend'] = friend_score
		obj['score'] += friend_score
		obj['details']['friend'] = friend_score
		
		# neighbors.append(obj)
		if 'UserID' in obj or 'Name' in obj:
			v = get_neighbor_or_create(obj)
			if v:
				neighbors[v.id] = obj
	return neighbors



def get_paper_bookmarks(users):
	bm_papers = {}
	for u in users:
		sequence = BookmarkSequence.objects.filter(user=u)
		if len(sequence):
			seq = sequence[0]
			bms = seq.all_bookmarks.split(',')
			if len(bms):
				if str(bms[-1]) == '':
					bms = list(bms[:-1])
				bm_papers[u.pk] = list(bms)
				print 'User #'+str(u.pk) + ' -> '+ u.name + ' = ' + str(len(bms)) + ' paper bookmarks'
			else:
				bm_papers[u.pk] = []
				print 'User #'+str(u.pk) + ' -> '+ u.name + ' = NO paper bookmarks'
		else:
			bm_papers[u.pk] = []
			print 'User #'+str(u.pk) + ' -> '+ u.name + ' = NO paper bookmarks'
	
	return bm_papers




def get_author_bookmarks(bm_papers, new_papers, old_papers):
	
	bm_authors = {}
	# Add paper authors to user's bookmarked authors
	for uid, paper_bms in bm_papers.iteritems():
		bm_authors[uid] = {}
		for contentID in paper_bms:
			# fetch paper, either new or old
			paper = None
			if contentID in new_papers:
				paper = new_papers[contentID]
				print 'new paper #' + str(paper['id'])
			elif contentID in old_papers:
				paper  = old_papers[contentID]
				print 'old paper #' + str(paper['id'])
			# add paper authors to user's bookmarked authors
			if paper:
				for author in paper['authorids']:
					if author not in bm_authors[uid]:
						bm_authors[uid][author] = 0
					bm_authors[uid][author] += 1
		print 'Added ' + str(len(bm_authors[uid])) +' author bookmarks for user #' + str(uid)

	return bm_authors



# 1. <user, neighbor> similarity
def get_user_user_sim(participants, users, soc_neighbors, bm_papers, bm_authors):
	B = []
	# bookmark overlap
	for user in participants:
		uid = user.id
		pbms1 = bm_papers[uid]
		sim_u1 = []
		for neighbor in users:
			vid = neighbor.id
			pbms2 = bm_papers[vid]
			
			if uid == vid:
				sim_u1.append(1.0)
			else:
				# Extend social neighbors and add explanations in details field
				if vid not in soc_neighbors[uid]:
					soc_neighbors[uid][vid] = { 'score': 0.0, 'details': {} }

				# Add score from social neighbors if exists
				sim_soc = soc_neighbors[uid][vid]['score']

				# Jaccard similarity. overlap between u and v's bookmarks
				sim_jac = 0.0
				if len(pbms1) and len(pbms2):
					sim_jac = float(len(list(set(pbms1) & set(pbms2)))) \
						 / len(set(pbms1 + pbms2))
					soc_neighbors[uid][vid]['score'] += sim_jac
					soc_neighbors[uid][vid]['details']['bm_overlap'] = sim_jac

				# If user bookmarked a talk from v in the past, increase similarity score
				sim_pastbm = 0.0
				if vid in bm_authors[uid]:
					sim_pastbm = bm_authors[uid][vid] * 0.1
					soc_neighbors[uid][vid]['score'] += sim_pastbm
					soc_neighbors[uid][vid]['details']['past_bm'] = sim_pastbm

				sim = sim_soc + sim_jac + sim_pastbm
				sim_u1.append(sim)

		# append current user's list to matrix B
		B.append(sim_u1)
			
	# Prepare for matrix factorization
	B = np.array(B)
	nB = B
	# print 'B is a ' +str(len(B)) + 'x' + str(len(B[0])) + ' matrix'
	# K = 3
	# nB = matrix_factorization(B, K, steps=100, alpha=0.0002, beta=0.02)
	# print 'nB is a ' +str(len(nB)) + 'x' + str(len(nB[0])) + ' matrix'
	return nB, soc_neighbors





def run():
	clear_db()
	event_ids = [149]
	
	for eventID in event_ids:		
		event = Event.objects.get(pk=eventID)
		talks = Talk.objects.all()
		print '\nEvent #' + str(eventID) + ' --> ' + event.title
		participants = get_participants(eventID) #[:3]
		users = User.objects.all()
		print 'Participants for ' + event.title + ' = ' + str(len(participants))
		
		print 'Fetching new papers ...'
		new_papers = get_new_papers(talks)
		print 'Fetched ' + str(len(new_papers)) + ' new papers'
		print 'Fetching old papers ...'
		old_papers = get_old_papers()
		print 'Fetched ' + str(len(old_papers)) + ' old papers'

		print '\n GET PAPER BOOKMARKS'
		bm_papers = get_paper_bookmarks(users)
		print '\n GET AUTHOR BOOKMARKS'
		bm_authors = get_author_bookmarks(bm_papers, new_papers, old_papers)

		print '\n GET FRIENDS and NEIGHBORS FROM SOCIAL API (Hyman)'
		soc_neighbors = {}
		for i, user in enumerate(participants):
			step = '(' + str(i+1) + '/' + str(len(participants)) + ')'
			print '\n' + step + ' ==> #' + str(user.pk) + ' - ' + user.name
			friends = get_friends(user.pk)
			# list of neighbors for current user
			soc_neighbors[user.pk] = get_social_neighbors(event.pk, user.pk, friends)
			# save_sim_user_neighbor(event, user, neighbors)

		print '\n CALCULATE USER-NEIGHBOR SIMILARITY'
		M, neighbors = get_user_user_sim(participants, users, soc_neighbors, bm_papers, bm_authors)

		save_sim_user_neighbor(M, event, participants, users, neighbors)



def save_sim_user_neighbor(M, event, participants, users, neighbors):
	count_v = 0
	for i, u in enumerate(participants):
		u_neighbors = neighbors[u.pk]
		for j, v in enumerate(users):
			original_score = u_neighbors[v.pk]['score'] if v.pk in u_neighbors else 0.0
			score = max(M[i][j], original_score)
			details = u_neighbors[v.pk]['details'] if v.pk in u_neighbors else {}
			explanations = json.dumps(details)
			
			sim_u_v = SimUserNeighbor(user=u, neighbor=v, event=event, 
				score=score, explanations=explanations)
			sim_u_v.save()
			count_v += 1
		print '=== SAVED ' + str(count_v )+ ' neighbors for '+ u.name



# SAVE NEIGHBORS

def get_neighbor_or_create(v):
	# neighbor = None
	# Try to find neighbor by ID
	if u'UserID' in v:
		try:
			# user already registered with original ID
			neighbor = User.objects.get(pk=v['UserID'])
			return neighbor
		except Exception, e:
			neighbor = None
	# Try to find neighbor by name
	if u'Name' in v:
		v_id = None
		try: 
			neighbor = User.objects.get(name=v['Name'])
			# print 'Found by name = ' + neighbor.name + ', new_id = ' + str(neighbor.id)
			# Only change if it comes with original UserID
			if v['UserID']:
				v_id = int(v['UserID']) 
				neighbor.id = v_id
				neighbor.type = 'original'
				neighbor.save()
				print '** Change user type, new id = ' + str(neighbor.pk) # + ' (matches ' + str(v['UserID']) + ')'
			return neighbor
		except Exception, e:
			if v['UserID']:
				new_id = User.objects.all().order_by('-id')[0].id + 1
				neighbor = User.objects.create(
					id = new_id,
					name = v['Name'],
					username = v['Name'].replace(' ', '_'),
					type = 'added'
				)
				print '++ Added new user -> ' + neighbor.name
				return neighbor
				

	# try:
	# 	# neighbor could be already saved as 'added' in cn-talks bc was found as author. Change id and type		
	# 	if 'Name' not in v:
	# 		print 'NO NAME'
	# 		return None;
	# 	neighbor = User.objects.get(name=v['Name'])
	# 	v_id = v['UserID'] if 'UserID' in v else User.objects.all().order_by('-id')[0].id + 1
	# 	neighbor.id = v_id
	# 	neighbor.type = 'original'
	# 	neighbor.save()
	# 	print '** Change user type, new id = ' + str(neighbor.pk) # + ' (matches ' + str(v['UserID']) + ')'
	# 	return neighbor
	# except:
	# 	# Neighbor doesn't exist, create user with type = 'added'
	# 	try:
	# 		new_id = User.objects.all().order_by('-id')[0].id + 1
	# 		neighbor = User.objects.create(
	# 			id = new_id,
	# 			name = v['Name'],
	# 			username = v['Name'].replace(' ', '_'),
	# 			type = 'added'
	# 		)
	# 		print '++ Added new user -> ' + neighbor.name
	# 		return neighbor
	# 	except:
	# 		# should not be here
	# 		print 'Fetched user'
	# 		print v
	# 		print 'User in DB'
	# 		user  = User.objects.get(pk=new_id)
	# 		print user.name + ', id = '+ str(user.pk)
	# 		return None

	

# def save_sim_user_neighbor(event, user, neighbors):	
# 	count_v = 0
# 	for v in neighbors:
# 		if v['score']:
# 			neighbor = get_neighbor_or_create(v)
# 			if neighbor:
# 				prev_sims = SimUserNeighbor.objects.filter(user=user).filter(neighbor=neighbor)
# 				if len(prev_sims) == 0:
# 					sim_u_v = SimUserNeighbor(user=user, neighbor=neighbor, score=v['score'],
# 						pub_sim = v['P'], co_auth = v['C'], interest = v['I'], geo_dist= v['G'],
# 						soc_ctx = v['S'], friend = v['friend'], event = event)
# 					sim_u_v.save()
# 					count_v += 1
# 	print '=== SAVED ' + str(count_v )+ ' neighbors for '+ user.name















