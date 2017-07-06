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
	SimUserTalk.objects.all().delete()


def get_new_papers(talks):
	print 'FETCH NEW TALKS'
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



def get_paper_bookmarks(users):
	bm_user_papers = {}
	paper_ids = []
	for u in users:
		seq = BookmarkSequence.objects.filter(user=u)
		if len(seq):
			bms = seq[0].all_bookmarks.split(',')
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
			elif uid in bm_user_papers and str(oid) in bm_user_papers[uid]:
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




def run():
	clear_db()
	print 'CALCULATE USER-TALK SIMILARITY'
	users = User.objects.all() #[:10]
	print 'Fetched ' + str(len(users)) + ' users'
	talks = Talk.objects.all().prefetch_related('talk_keywords') #[:10]
	new_papers = get_new_papers(talks)
	print 'Fetched ' + str(len(new_papers)) + ' new papers'
	old_papers = get_old_papers()
	print 'Fetched ' + str(len(old_papers)) + ' old papers'	

	print '\nEXTRACT BOOKMARKED PAPERS'
	bm_user_papers, paper_ids = get_paper_bookmarks(users)
	
	# print '\nEXTRACT BOOKMARKED AUTHORS'
	# bm_user_author = get_author_bookmarks(bm_user_papers, new_papers, old_papers)

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




