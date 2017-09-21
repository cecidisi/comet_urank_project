# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import urllib2
import requests
import unicodedata
import datetime
import time

from bs4 import BeautifulSoup as bs
from conf_navigator.classes.bcolors import *
from upmc_urank.models import *


def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')

def run():
	print 'RUN'
	clean_db()
	term = 'migraine'
	retstart = 0
	retmax = 100
	count = 10000
	search(term, retstart, retmax, count)


def clean_db():
	Affiliation.objects.all().delete()
	Author.objects.all().delete()
	PublicationDetails.objects.all().delete()
	Article.objects.all().delete()



def search(term, retstart, retmax, count=0):
	base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	url_search = base_url + 'esearch.fcgi?db=pubmed&usehistory=y&term=' + term + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)
	start1 = time.time()

	# Search Request
	print 'eSearching ...'
	resp = requests.get(url_search)
	soup = bs(resp.text, 'xml')
	_count = int(soup.find('Count').get_text())
	count = min(count, _count) if count else _count
	query_key = soup.find('QueryKey').get_text()
	web_env = soup.find('WebEnv').get_text()
	print_green('Finished SEARCH = ' + str(time.time() - start1))
	print_blue('Count = ' + str(count))
	print_blue('Query Key = ' + str(query_key))
	print_blue('WebEnv = ' + str(web_env))
	fetch(base_url, query_key, web_env, retstart, retmax, count)
	


def fetch(base_url, query_key, web_env, retstart, retmax, count):

	tot_batches = int(count / retmax)
	# Fetch in batches
	start1 = time.time()
	while retstart < count:
		# Save articles after fetching a whole batch
		papers = []
		run = (retstart / retmax) + 1
		url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)

		print 'eFetching ...'
		start2 = time.time()
		resp = requests.get(url_fetch)
		end_req = time.time()

		print_green('#' +str(run)+'/'+ str(tot_batches) +' Finished FETCH batch ' + str(end_req - start2))

		# Parse Response
		soup = bs(resp.text.encode('utf-8'), 'xml')
		raw_papers = soup.find_all('PubmedArticle')
		print 'Fetched ' + str(len(raw_papers)) + ' papers'
		
		for i, p in enumerate(raw_papers):
			obj = {}
			art = p.MedlineCitation.Article
			# PMID
			obj['pmid'] = int(p.MedlineCitation.PMID.get_text())
			# Publication Type
			obj['pub_type'] = art.PublicationType.get_text()
			# Title
			obj['title'] =  art.ArticleTitle.get_text()
			# Abstract
			obj['abstract'] = ''
			if art.Abstract:
				abstract_chunks = art.Abstract.find_all('AbstractText')
				for j, chunk in enumerate(abstract_chunks):
					label = chunk.get('Label') or ''
					if label:
						obj['abstract'] += label + ': '
					obj['abstract'] += chunk.get_text() + '\n'
				obj['abstract'] = obj['abstract'][:-1]
			# Authors
			obj['authors'] = []
			if art.AuthorList:
				author_list = art.AuthorList.find_all('Author')
				for a in author_list:
					if a.get('ValidYN') == 'Y':
						affiliation = ''
						if a.AffiliationInfo and a.AffiliationInfo.Affiliation:
							affiliation = a.AffiliationInfo.Affiliation.get_text()
						try:
							obj['authors'].append((
								a.LastName.get_text(),
								a.ForeName.get_text(),
								a.Initials.get_text(),
								affiliation
							))
						except:
							if a.CollectiveName:
								obj['authors'].append((a.CollectiveName.get_text(), '', '', ''))
			# Publication Details
			obj['publication_details'] = {
				'journal': '', 'abbr': '', 'issn': '', 'volume': '', 'issue': '', 'date_str': '', 'year': None
			}
			if art.Journal :
				obj['publication_details']['journal'] = art.Journal.Title.get_text()
				if art.Journal.ISOAbbreviation:
					obj['publication_details']['abbr'] = art.Journal.ISOAbbreviation.get_text()
				if art.Journal.ISSN:
					obj['publication_details']['issn'] = art.Journal.ISSN.get_text()
				if art.Journal.JournalIssue.Volume:
					obj['publication_details']['volume'] = art.Journal.JournalIssue.Volume.get_text()
				if art.Journal.JournalIssue.Issue:
					obj['publication_details']['issue'] = art.Journal.JournalIssue.Issue.get_text()
				if art.Journal.JournalIssue.PubDate.Year:
					year = art.Journal.JournalIssue.PubDate.Year.get_text()
					date_str = ''
					if art.Journal.JournalIssue.PubDate.Month:
						month = art.Journal.JournalIssue.PubDate.Month.get_text()
						date_str += month
						if art.Journal.JournalIssue.PubDate.Day:
							day = art.Journal.JournalIssue.PubDate.Day.get_text()
							date_str += ' ' + day
						date_str += ', ' 
					date_str += str(year)
					# date_str format = Jun 12, 2000
					obj['publication_details']['date_str'] = date_str
					obj['publication_details']['year'] = int(year)

			# Author Keywords
			author_kw = []
			if p.MedlineCitation.KeywordList:
				for kw in p.MedlineCitation.KeywordList.find_all('Keyword'):
					author_kw.append(kw.get_text())
			obj['author_keywords'] = '; '.join(author_kw)
			papers.append(obj)

			# IDs (doi)
			if p.PubmedData.ArticleIdList:
				doi = p.PubmedData.ArticleIdList.find('ArticleId', { 'IdType': 'doi' })
				obj['doi'] = doi.get_text() if doi else None

		retstart += retmax
		print_green('#' +str(run)+'/'+ str(tot_batches) +' Finished processing papers = ' + str(time.time() - end_req))
		start2 = time.time()
		save_papers(papers)
		print_green('Time to process articles = ' + str(time.time() - start2))
		

	print_blue('TOTAL TIME ELAPSED = ' + str(time.time() - start1) + ' sec.')



def save_papers(papers):
	start1 = time.time()
	for idx, p in enumerate(papers):
		authors = []
		for a in p['authors']:
			# Affiliation
			affiliation = None
			if a[3] != '':
				try:
					affiliation, created = Affiliation.objects.get_or_create(name=a[3])
				except Exception, e:
					print a[3]
					print_red(str(e))
			# Author
			try:
				author, created = Author.objects.get_or_create(
					last_name = a[0],
					fore_name = a[1],
					initials = a[2]
				)
				# Link author to affiliation
				if affiliation and not author.affiliations.filter(pk=affiliation.pk).exists():
					author.affiliations.add(affiliation)
				authors.append(author)
			except Exception, e:
				print a
				print_red(str(e))

		# Publication Details
		pd = p['publication_details']
		pub_details = PublicationDetails(
			journal = pd['journal'],
			abbr = pd['abbr'],
			issn = pd['issn'],
			volume = pd['volume'],
			issue = pd['issue'],
			date_str = pd['date_str'],
			year = pd['year']
		)
		pub_details.save()

		# Article
		try:
			article = Article.objects.create(
				pmid = p['pmid'],
				doi = p['doi'],
				title = p['title'],
				abstract = p['abstract'],
				pub_type = p['pub_type'],
				pub_details = pub_details,
				author_keywords = p['author_keywords']
			)
			# Link article to authors
			for a in authors:
				article.authors.add(a)
			# print 'Saved article pmid = ' + str(article.pmid)
		except Exception, e:
			print_red(str(e))

		
	print 'Saved ' + str(len(papers)) + ' articles'











