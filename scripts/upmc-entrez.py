# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import urllib2
import requests
import unicodedata

import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient

from bs4 import BeautifulSoup as bs
from conf_navigator.classes.bcolors import *


def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')



def run():
	print_red('RUN')
	base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	search_url = 'esearch.fcgi?db=pubmed&usehistory=y'
	fetch_url = 'efetch.fcgi?db=pubmed&rettype=abstract&retmode=text'
	term = 'migraine'
	retstart = 0
	retmax = 100

	url_search = base_url + 'esearch.fcgi?db=pubmed&usehistory=y&term=' + term + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)
	start1 = time.time()

	# Search Request
	resp = requests.get(url_search)
	soup = bs(resp.text, 'xml')
	count =  int(soup.find('Count').get_text())
	query_key = soup.find('QueryKey').get_text()
	web_env = soup.find('WebEnv').get_text()
	print_red('Finished SEARCH = ' + str(time.time() - start1))
	print_blue('Count = ' + str(count))
	print_blue('Query Key = ' + str(query_key))
	print_blue('WebEnv = ' + str(web_env))
	

	papers = []
	tot_batches = int(count / retmax)
	# Fetch in batches
	while retstart < count:
		run = (retstart / retmax) + 1
		url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)

		start2 = time.time()
		resp = requests.get(url_fetch)
		end_req = time.time()

		print_red('#' +str(run)+'/'+ str(tot_batches) +' Finished FETCH batch ' + str(end_req - start2))

		# Parse Response
		soup = bs(resp.text.encode('utf-8'), 'xml')
		raw_papers = soup.find_all('PubmedArticle')
		print_blue('Fetched ' + str(len(raw_papers)) + ' papers')
		
		for i, p in enumerate(raw_papers):
			art = p.MedlineCitation.Article
			# Title
			title =  art.ArticleTitle.get_text()
			# Abstract
			abstract = ''
			if art.Abstract:
				abstract_chunks = art.Abstract.find_all('AbstractText')
				for j, chunk in enumerate(abstract_chunks):
					label = chunk.get('Label') or ''
					if label:
						abstract += label + ': '
					abstract += chunk.get_text() + '\n'
				abstract = abstract[:-1]
			# Authors
			authors = []
			if art.AuthorList:
				author_list = art.AuthorList.find_all('Author')
				for a in author_list:
					if a.get('ValidYN') == 'Y':
						affiliation = ''
						if a.AffiliationInfo and a.AffiliationInfo.Affiliation:
							affiliation = a.AffiliationInfo.Affiliation.get_text()
						try:
							authors.append((
								a.LastName.get_text(),
								a.ForeName.get_text(),
								a.Initials.get_text(),
								affiliation
							))
						except:
							if a.CollectiveName:
								authors.append((a.CollectiveName.get_text(), '', '', ''))
			# Publication Details
			if art.Journal :
				journal = art.Journal.Title.get_text()
				abbr = ''
				if art.Journal.ISOAbbreviation:
					abbr = art.Journal.ISOAbbreviation.get_text()
				issn = ''
				if art.Journal.ISSN:
					issn = art.Journal.ISSN.get_text()
				volume = ''
				if art.Journal.JournalIssue.Volume:
					volume = art.Journal.JournalIssue.Volume.get_text()
				issue = ''
				if art.Journal.JournalIssue.Issue:
					issue = art.Journal.JournalIssue.Issue.get_text()
				date = ''
				if art.Journal.JournalIssue.PubDate.Year:
					year = art.Journal.JournalIssue.PubDate.Year.get_text()
					date += year
				if art.Journal.JournalIssue.PubDate.Month:
					month = art.Journal.JournalIssue.PubDate.Month.get_text()
					date += '/' + month				
					if art.Journal.JournalIssue.PubDate.Day:
						day = art.Journal.JournalIssue.PubDate.Day.get_text()
						date += '/' + day

			# Author Keywords
			author_kw = []
			for kw in p.find_all('Keyword'):
				author_kw.append(kw.get_text())

			# print '\n '+ str(i+1) +'. ================================'
			# print 'JOURNAL: ' + journal
			# print abbr + ' ' + issn + ' ' + volume + ' ' + issue + ' ' + date
 			# print 'TITLE: ' + title
			# print 'ABSTRACT: ' +abstract
			# print 'AUTHORS: ' + '; '.join([a[0]+' '+a[1] for a in authors])
			# print 'AUTHOR KEYWORDS: ' + '; '.join(author_kw)
		
			
		retstart += retmax
		print_red('#' +str(run)+'/'+ str(tot_batches) +' Finished processing papers = ' + str(time.time() - end_req))

	print_red('TOTAL TIME ELAPSED = ' + str(time.time() - start1) + ' sec.')

		
	# 	print 'VENUE'
	# 	print venue
	# 	print "TITLE"
	# 	print title
	# 	print 'AUTHORS'
	# 	print authors
	# 	print 'AUTHORS INFO'
	# 	print author_info
	# 	print 'ABSTRACT'
	# 	print abstract
	# 	print 'UIDS'
	# 	for uid in uids:
	# 		print uid





	# http_client = AsyncHTTPClient()
	# http_client.fetch(url_fetch, handle_response)
	# tornado.ioloop.IOLoop.instance().start()




	'''  EXAMPLE
	1. Neurol Int. 2017 Jun 23;9(2):7015. doi: 10.4081/ni.2017.7015. eCollection 2017
	Jun 23.

	Somatoform Dissociation, Fatigue Severity and Pain Behavior Compared in Patients
	with Migraine Headache and in Healthy Individuals.

	Fattahzadeh-Ardalani G(1), Aghazadeh V(2), Atalu A(1), Abbasi V(1).

	Author information:
	(1)Department of Neurology, Ardabil University of Medical Sciences, Ardabil,
	Iran.
	(2)Young Researchers Club and Elite Club, Ardabil Branch, Islamic Azad
	University, Ardabil, Iran.

	The prevalence of migraine in the world is about 15 and 7% among women and men,
	respectively. The purpose of this study was comparison of somatoform
	dissociation, fatigue severity and pain behavior in patients with migraine
	headache and its relationship with coping strategies. This descriptive analytical
	study has been done on 120 patients with migraine headache and 120 healthy
	subjects were selected randomly. Data collected by somatoform dissociation
	questionnaire (SDQ-20), fatigue severity scale, pain behavior scale and coping
	strategies scale. For data analysis we used SPSS.19. The means of the somatoform
	dissociation, pain behavior scale, help searching subscale and pain compliant in
	migraine and healthy subjects were statistically significant. There was not
	significant difference in avoidance subscales between the two groups. Comparison
	of fatigue severity in patients with migraine and control group was meaningful.
	There was significant positive correlation between all four scales and coping
	strategies. It seems that these symptoms can play an important role in this
	disease; thus, their careful evaluation in the treatment of migraine headache is
	essential.

	DOI: 10.4081/ni.2017.7015
	PMCID: PMC5505118
	PMID: 28713529
	'''





