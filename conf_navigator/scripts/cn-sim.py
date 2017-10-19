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



def get_new_papers(talks):
	new_papers = {}
	# Fetch papers in DB (future items)
	talks = Talk.objects.all().prefetch_related('talk_keywords') #[:10]
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
		print 'Added new paper #' + str(paper['id']) + ' -- ' + paper['title']
	return new_papers



def get_old_papers():
	print 'FETCH OLD PAPERS'
	old_papers = {}
	for op in OldPaper.objects.all():
		old_paper = {
			'id': op.pk,
			'title': op.title, 
			'abstract': op.abstract,
			'authorids': [int(author) for author in op.authorids.split(',')],
			'keywords': json.loads(op.keyword_str)
		}
		old_papers[op.pk] = old_paper
	return old_papers

	# print len(paper_ids)
	# old_papers = {}
	# ke = keyword_extractor({ 'stopwords': stopwords })
	# idx = 0
	# # print paper_ids[0]
	# for contentID in paper_ids:  #[:10]:
	# 	if contentID not in new_papers:
	# 		# print 'Fetch paper for contenID = ' + str(contentID)
	# 		paper = fetch_paper(contentID)
	# 		if paper:
	# 			# print 'Fetched old paper #' + str(paper['id']) + ' -- ' + paper['title']
	# 			old_papers[contentID] = paper
	# 			ke.add_document(paper)
	# 			old_papers[contentID]['index'] = idx
	# 			idx += 1
	# 		else:
	# 			print ' No paper found for contentID = ' + str(contentID)

	# print 'FETCHED ' + str(len(old_papers)) + ' OLD PAPERS'
	# ke.extract()
	# for contentID, paper in old_papers.iteritems():
	# 	old_papers[contentID]['keywords'] = ke.get_document_keywords(paper['index'])
	# 	print 'Extended old paper #' +str(contentID)+ ' with keywords = ' + str(len(old_papers[contentID]['keywords']))
	# return old_papers


def fetch_paper(contentID):
	url_temp = "http://halley.exp.sis.pitt.edu/cn3/social_api_getcontents.php?cid=[contentID]"
	url = url_temp.replace('[contentID]', str(contentID))
	resp = urllib2.urlopen(url).read()
	soup = bs(resp, 'lxml')
	if soup.find('title') and soup.find('title').get_text() != '':
		return {
			'id': contentID,
			'title': soup.find('title').get_text(),
			'abstract': soup.find('abstract').get_text(),
			'authorids': soup.find('authorids').get_text().split(',')[:-1]
		}
	return None


def get_paper_bookmarks(users):
	bm_user_papers = {}
	paper_ids = []
	for u in users:
		seq = BookmarkSequence.objects.filter(user=u)[0]
		bms = seq.all_bookmarks.split(',')
		if len(bms):
			if str(bms[-1]) == '':
				bms = list(bms[:-1])
			bm_user_papers[u.pk] = list(bms)
			paper_ids = paper_ids + list(bms)
			print 'User #'+str(u.pk) + ' -> '+ u.name + ' = ' + str(len(bms)) + ' paper bookmarks'
		else:
			bm_user_papers[u.pk] = []
			print 'User #'+str(u.pk) + ' -> '+ u.name + ' = NO paper bookmarks'
	paper_ids = list(set(paper_ids))
	return bm_user_papers, paper_ids



def get_author_bookmarks(bm_user_papers, new_papers, old_papers):
	bm_user_author = {}
	# Add paper authors to user's bookmarked authors
	for uid, paper_bms in bm_user_papers.iteritems():
		bm_user_author[uid] = {}
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
					if author not in bm_user_author[uid]:
						bm_user_author[uid][author] = 0
					bm_user_author[uid][author] += 1
		print 'Added ' + str(len(bm_user_author[uid])) +' author bookmarks for user #' + str(uid)

	return bm_user_author



# 1. <user, neighbor> similarity
def get_user_user_sim(users, bm_user_papers, bm_user_author):
	B = []
	# bookmark overlap
	for user in users:
		uid = user.id
		pbms1 = bm_user_papers[uid]
		sim_u1 = []
		for neighbor in users:
			vid = neighbor.id
			pbms2 = bm_user_papers[vid]
			if uid == vid:
				sim_u1.append(1.0)
			else:
				# Jaccard similarity
				sim = 0.0
				if len(pbms1) and len(pbms2):
					sim = float(len(list(set(pbms1) & set(pbms2)))) \
						 / len(set(pbms1 + pbms2))
				# If user bookmarked a talk from v in the past, increase similarity score
				if vid in bm_user_author[uid]:
					sim += bm_user_author[uid][vid] * 0.1
				sim_u1.append(sim)
		B.append(sim_u1)
			
	# Prepare for matrix factorization
	B = np.array(B)
	print 'B is a ' +str(len(B)) + 'x' + str(len(B[0])) + ' matrix'
	K = 3
	nB = matrix_factorization(B, K, steps=1000, alpha=0.0002, beta=0.02)
	print 'nB is a ' +str(len(nB)) + 'x' + str(len(nB[0])) + ' matrix'
	return nB



# user similar to old paper if is author or bookmarked
def get_user_oldpaper_sim(users, old_papers, bm_user_papers):
	sim_u_op = {}
	for u in users:
		uid = u.pk
		if uid not in sim_u_op:
			sim_u_op[uid] = {}
		for oid, paper in old_papers.iteritems():
			score = 0.0
			# check if user is author
			if uid in paper['authorids']:
				score = 1.0
			# check if user bookmarked old paper
			elif uid in bm_user_papers and oid in bm_user_papers[uid]:
				score = 0.8
			sim_u_op[uid][oid] = score
	return sim_u_op



# 2. <old_doc, new_doc> similarity
def get_item_item_sim(old_papers, new_papers):
	print 'Computing computing item-item similarity ...'
	sim_papers = {}
	for nid, pnew in new_papers.iteritems():
		#  add entry for old paper
		if nid not in sim_papers:
			sim_papers[nid] = {}
		for oid, pold in old_papers.iteritems():	
			kw_old = pold['keywords']
			kw_new = pnew['keywords']
			prod_norm = get_eucliden_norm(kw_old) * get_eucliden_norm(kw_new)
			# print 'prod norm = ' + str(prod_norm)
			for k in set(kw_old.keys() + kw_new.keys()):
				tf1 = float(kw_old[k]['tf']) if k in kw_old else 0.0
				tf2 = float(kw_new[k]['tf']) if k in kw_new else 0.0
				sim_papers[nid][oid] = (tf1 * tf2) / prod_norm if prod_norm else 0.0
				# print 'tf1 = ' + str(tf1) + '; tf2 = ' + str(tf2) + ' tot = ' + str(sim_papers[nid][oid])	
	return sim_papers


def get_eucliden_norm(doc_keywords):
	acum_squares = 0.0
	for key, k in doc_keywords.iteritems():
		acum_squares += pow(k['tf'], 2)
	return math.sqrt(float(acum_squares))



# 3. <v, new_item> similarity
def get_user_item_sim(users, talks, new_papers, old_papers, bm_user_papers):
	sim_user_oldpapers = get_user_oldpaper_sim(users, old_papers, bm_user_papers)
	sim_new_old_papers = get_item_item_sim(old_papers, new_papers)

	Q = np.zeros((len(users), len(talks)))
	print 'Compute user-item matrix'
	for i, user in enumerate(users):
		uid = user.id
		for j, talk in enumerate(talks):
			pid = talk.id
			paper = new_papers[pid]
			# Check if user is author of new paper
			if uid in paper['authorids']:
				Q[i][j] = 1.0
			# check if user bookmarked new paper
			elif uid in bm_user_papers and pid in bm_user_papers[uid]:
				Q[i][j] = 0.8
			# check similarity between user & old papers and between old and new papers
			else:
				acum = 0.0
				n = 0.0
				# for each old paper similar to current user
				if uid in sim_user_oldpapers:
					for oid, sim_u_op in sim_user_oldpapers[uid].iteritems():
						if oid in sim_new_old_papers[pid]:
							# sim <user, old paper> * sim <new paper, old paper>
							acum += sim_u_op * sim_new_old_papers[pid][oid]
							n += 1.0
				Q[i][j] = acum/n if acum else 0.0
	return Q



def clear_db():
	SimUserNeighbor.objects.all().delete()
	SimUserTalk.objects.all().delete()



def main():	
	clear_db()
	users = User.objects.all() #[:10]
	print 'EXTRACT BOOKMARKED PAPERS'
	bm_user_papers, paper_ids = get_paper_bookmarks(users)
	new_papers = get_new_papers()
	print 'Fetched ' + str(len(new_papers)) + ' new papers'
	old_papers = get_old_papers(paper_ids, new_papers)
	print 'Fetched ' + str(len(old_papers)) + ' old papers'
	print 'EXTRACT BOOKMARKED AUTHOR'
	bm_user_author = get_author_bookmarks(bm_user_papers, new_papers, old_papers)

	
	Muv = get_user_user_sim(users, bm_user_papers, bm_user_author)
	print 'Muv is a ' + str(len(Muv)) + 'x' + str(len(Muv[0])) + ' matrix'
	Mvi = get_user_item_sim(users, talks, new_papers, old_papers, bm_user_papers)
	print 'Mvi is a ' + str(len(Mvi)) + 'x' + str(len(Mvi[0])) + ' matrix'
	# print Mui
	# Mui = np.dot(Muv, Mvi)
	# print 'Mui is a ' + str(len(Mui)) + 'x' + str(len(Mui[0])) + ' matrix'
	# print Mui

	for i, user in enumerate(users):
		#  save user-neighbor sim
		count_v = 0
		for j, neighbor in enumerate(users):
			score = Muv[i][j]
			if score and i != j:
				sim_u_v = SimUserNeighbor(user=user, neighbor=neighbor, score=score)
				sim_u_v.save()
				count_v += 1
		print 'Saved ' + str(count_v )+ ' neighbors for user #'+str(user.id)
		# save neighbor-paper sim (i.e. user-talk)
		count_p = 0
		for j, talk in enumerate(talks):
			score = Mvi[i][j]
			if score:
				sim_v_p = SimUserTalk(user=user, talk=talk, score=score)
				sim_v_p.save()
				count_p += 1
		print 'Saved '+str(count_p)+' papers for user #'+str(user.id)



def run():
	# main()
	main2()


def main2():
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
			neighbors = get_similar_users(event.pk, user.pk)
			save_sim_user_neighbor(event, user, neighbors)

	print 'GET BOOKMARKED PAPERS'
	users = User.objects.all() #[:10]
	bm_user_papers, paper_ids = get_paper_bookmarks(users)
	new_papers = get_new_papers()
	print 'Fetched ' + str(len(new_papers)) + ' new papers'
	old_papers = get_old_papers(paper_ids, new_papers)
	print 'Fetched ' + str(len(old_papers)) + ' old papers'
	print 'EXTRACT BOOKMARKED AUTHOR'
	bm_user_author = get_author_bookmarks(bm_user_papers, new_papers, old_papers)

	Mvi = get_user_item_sim(users, talks, new_papers, old_papers, bm_user_papers)
	print 'Mvi is a ' + str(len(Mvi)) + 'x' + str(len(Mvi[0])) + ' matrix'

	for i, user in enumerate(users):
		# save neighbor-paper sim (i.e. user-talk)
		count_p = 0
		for j, talk in enumerate(talks):
			score = Mvi[i][j]
			if score:
				sim_v_p = SimUserTalk(user=user, talk=talk, score=score)
				sim_v_p.save()
				count_p += 1
		print 'Saved '+str(count_p)+' papers for user #'+str(user.id)






def get_participants(eventID):
	participants = User.objects.filter(events__pk=eventID)
	return participants



def save_sim_user_neighbor(event, user, neighbors):	
	count_v = 0
	for v in neighbors:
		if v['score']:
			neighbor = check_neighbor_exists(v)
			if neighbor:
				sim_u_v = SimUserNeighbor(user=user, neighbor=neighbor, score=v['score'],
					pub_sim = v['P'], co_auth = v['C'], interest = v['I'], geo_dist= v['G'],
					soc_ctx = v['S'], event = event)
				sim_u_v.save()
				count_v += 1
	print 'Saved ' + str(count_v )+ ' neighbors for '+ user.name



def check_neighbor_exists(v):
	neighbor = None
	if v['UserID']:
		try:
			# user already registered with original ID
			neighbor = User.objects.get(pk=v['UserID'])
			return neighbor
		except:
			try:
				# see if neighbor already saved as 'added' in cn-talks bc was found as author. Change id and type
				neighbor = User.objects.get(name=v['Name'])
				neighbor.id = v['UserID']
				neighbor.type = 'original'
				neighbor.save()
				print '** Change user type, new id = ' + str(neighbor.pk) # + ' (matches ' + str(v['UserID']) + ')'
				return neighbor
			except:
				neighbor = None
	else:
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
			print 'Fetched user'
			print v
			print 'User in DB'
			user  = User.objects.get(pk=new_id)
			print user.name + ', id = '+ str(user.pk)
			return None




def get_similar_users(cid, uid):
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
		for i, attr in enumerate(row.split(',')):
			obj['score'] = 0.0
			if header[i] in scores:
				sub_score = float(attr) if attr != '' else 0.0
				obj[header[i]] = sub_score
				obj['score'] += sub_score
			elif header[i] == 'AuthorID' or header[i] == 'UserID':
				obj[header[i]] = int(attr) if attr != '' else None
			else: # Name
				obj[header[i]] = attr
		neighbors.append(obj)
	return neighbors




def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')



def test_fetch_empty_paper():
	print fetch_paper(9378)

