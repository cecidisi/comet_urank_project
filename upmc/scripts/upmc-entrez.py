# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import time
import urllib2
import requests
import unicodedata
import datetime
import time
import multiprocessing as mp
from django import db
from bs4 import BeautifulSoup as bs
from functools import partial
from itertools import groupby, chain
from helper.bcolors import *
from helper.pretty_time import *
from upmc.models import *
from helper.mp_progress_tracker import *


def run(*args):
	print 'RUN'
	start = time.time()
	clean_db()
	term = 'migraine'
	count = 1000 	# Total number of items
	retmax = 100	# Number items per batch
	if 'get-all' in args:
		count = 0
		retmax = 100
	
	cores = max(10, int(mp.cpu_count() *.75))
	base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	query_key, web_env, max_count = search(base_url, term)
	count = min(count, max_count) if count else max_count
	# fetch_test(base_url, query_key, web_env, retmax, count, cores)
	papers = fetch_parallel(base_url, query_key, web_env, retmax, count, cores)
	# papers = fetch_serial(base_url, query_key, web_env, retmax, count, cores)
	print_blue('Total Time Elapsed = ' + secToMMSS(time.time() - start))



def clean_db():
	Affiliation.objects.all().delete()
	Author.objects.all().delete()
	# PublicationDetails.objects.all().delete()
	Article.objects.all().delete()
	print_blue('Finished cleaning DB')


# Call eSearch on entrez api
# Returns query_key and web_env, necessary to later get abstracts with efeatch
def search(base_url, term):	
	url_search = base_url + 'esearch.fcgi?db=pubmed&usehistory=y&term=' + term
	print 'eSearching ...'

	start1 = time.time()
	resp = requests.get(url_search)
	soup = bs(resp.text, 'xml')
	query_key = soup.find('QueryKey').get_text()
	web_env = soup.find('WebEnv').get_text()
	max_count = int(soup.find('Count').get_text())

	print_green('Finished SEARCH = ' + str(time.time() - start1))
	print_blue('Query Key = ' + str(query_key))
	print_blue('WebEnv = ' + str(web_env))
	print_blue('max_count = ' + str(max_count))
	return (query_key, web_env, max_count)
	



def fetch_worker(url_fetch, retmax, batches, i):
	retstart = i * retmax
	url_fetch = url_fetch.replace('[retstart]', str(retstart))
	max_attempts = 3
	cur_attempt = 1
	items = []
	while(cur_attempt <= max_attempts and len(items) == 0):
		resp = requests.get(url_fetch)
		soup = bs(resp.text.encode('utf-8'), 'xml')
		items = soup.find_all('PubmedArticle')
		cur_attempt += 1
	# print 'Batch (' + str(i+1) + '/' + str(batches) + ') --> Fetched ' + str(len(items)) + ' items ('+str(cur_attempt-1)+' attempt/s) [retstart = ' + str(retstart) + ', retmax = ' + str(retmax) +']'
	paper_count = 0
	papers = []
	for p in items:
		paper = parse_paper(p)
		if paper:
			paper = save_paper(paper)
			if paper:
				paper_count += 1
				papers.append(paper)
	# print 'Batch (' + str(i+1) + '/' + str(batches) + ') --> Saved ' +str(paper_count)+ ' items'
	# return paper_count
	return papers



def fetch_serial(base_url, query_key, web_env, retmax, count, cores):
	print 'eFetching serial ...'
	batches = count/retmax
	url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env  + '&retmax=' + str(retmax) + '&retstart=[retstart]'
	
	tmsp1 = time.time()
	all_papers = []
	for i in range(batches):
		jobs = fetch_worker(url_fetch, retmax, batches, i)
		all_papers = list(chain(all_papers, jobs))

	tmsp2 = time.time() - tmsp1
	paper_count = len(all_papers)
	print_green('Total papers =  ' + str(paper_count) + '; eFetch Time = ' + secToMMSS(tmsp2))
	return all_papers



def fetch_parallel(base_url, query_key, web_env, retmax, count, cores):
	batches = count/retmax
	jobs = []
	db.connections.close_all()
	print 'eFetching ' + str(count) +' items --> processes =  ' +str(cores)+ ', batches = ' + str(batches)

	# Set progressbar
	tracker = mpProgressTracker(title='Fetching & Saving', total = batches)
	tmsp1 = time.time()
	url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env  + '&retmax=' + str(retmax) + '&retstart=[retstart]'
	worker = partial(fetch_worker, url_fetch, retmax, batches)
	pool = mp.Pool(processes=cores)
	jobs = pool.map_async(worker, range(batches))
	# Track Progress
	tracker.track(jobs)
	# Close pool
	pool.close()
	pool.join()

	tmsp2 = time.time() - tmsp1
	from functools import reduce
	all_papers = list(chain.from_iterable(jobs.get()))
	# paper_count = reduce((lambda x, y: x+y), jobs.get())
	paper_count = len(all_papers)
	print_green('Total papers =  ' + str(paper_count) + '; eFetch Time = ' + secToMMSS(tmsp2))
	return all_papers
	

'''
Parse XML to JSON format
'''
def parse_paper(p):
	paper = {}
	art = p.MedlineCitation.Article
	# PMID
	paper['pmid'] = int(p.MedlineCitation.PMID.get_text())
	# Publication Type
	paper['pub_type'] = art.PublicationType.get_text()
	# Title
	paper['title'] =  art.ArticleTitle.get_text()
	# Abstract
	paper['abstract'] = ''
	if art.Abstract:
		abstract_chunks = art.Abstract.find_all('AbstractText')
		for j, chunk in enumerate(abstract_chunks):
			label = chunk.get('Label') or None
			if label:
				paper['abstract'] += label + ': '
			paper['abstract'] += chunk.get_text() + '\n'
		paper['abstract'] = paper['abstract'][:-1]

	# If paper doesn't have extract, exclude
	if paper['abstract'] == '':
		return None

	# Authors
	paper['authors'] = []
	if art.AuthorList:
		author_list = art.AuthorList.find_all('Author')
		for a in author_list:
			if a.get('ValidYN') == 'Y':
				affiliation = ''
				if a.AffiliationInfo and a.AffiliationInfo.Affiliation:
					affiliation = a.AffiliationInfo.Affiliation.get_text()
				try:
					paper['authors'].append((
						a.LastName.get_text(),
						a.ForeName.get_text(),
						a.Initials.get_text(),
						affiliation
					))
				except:
					if a.CollectiveName:
						paper['authors'].append((a.CollectiveName.get_text(), '', '', ''))

	if len(paper['authors']):
		paper['authors_list'] = '; '.join((a[0]+', '+a[1]) for a in paper['authors'])
	else: 
		paper['authors_list'] = ''		

		
	# Publication Details
	paper['publication_details'] = {
		'journal': '', 'abbr': '', 'issn': '', 'volume': '', 'issue': '', 'date_str': '', 'year': None
	}
	if art.Journal :
		paper['publication_details']['journal'] = art.Journal.Title.get_text()
		if art.Journal.ISOAbbreviation:
			paper['publication_details']['abbr'] = art.Journal.ISOAbbreviation.get_text()
		if art.Journal.ISSN:
			paper['publication_details']['issn'] = art.Journal.ISSN.get_text()
		if art.Journal.JournalIssue.Volume:
			paper['publication_details']['volume'] = art.Journal.JournalIssue.Volume.get_text()
		if art.Journal.JournalIssue.Issue:
			paper['publication_details']['issue'] = art.Journal.JournalIssue.Issue.get_text()
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
			paper['publication_details']['date_str'] = date_str
			paper['publication_details']['year'] = int(year)


	# Author Keywords
	author_kw = []
	if p.MedlineCitation.KeywordList:
		for kw in p.MedlineCitation.KeywordList.find_all('Keyword'):
			author_kw.append(kw.get_text())
	paper['author_keywords'] = '; '.join(author_kw)
	# IDs (doi)
	if p.PubmedData.ArticleIdList:
		doi = p.PubmedData.ArticleIdList.find('ArticleId', { 'IdType': 'doi' })
		paper['doi'] = doi.get_text() if doi else None

	return paper




def clean_text(text):
	if isinstance(text, str):
		return text
	# Replace smart quotes and other known unicode characters
	text = text.replace(u'\u201c', '"').replace(u'\u201d', '"') \
		.replace("‘", "'").replace("’", "'") \
		.replace(u'\xe2??', "'")
	return unicodedata.normalize('NFKD', text).encode('ascii','ignore')


	

'''
Saved paper to DB
'''
def save_paper(paper):
	from warnings import filterwarnings
	import MySQLdb as Database
	filterwarnings('ignore', category = Database.Warning)

	authors = []
	for a in paper['authors']:
		# Affiliation
		affiliation = None
		if a[3] != '':
			affiliation = None
			try:
				affiliation = Affiliation.objects.get(name=a[3])
			except ObjectDoesNotExist:
				affiliation = Affiliation(name=a[3])
				affiliation.save()
			
		# Author		
		author = None
		try:
			author = Author.objects.get(last_name=a[0], fore_name=a[1])
		except MultipleObjectsReturned, e:
			print_red(str(e))
			author = Author.objects.filter(last_name=a[0]).filter(fore_name=a[1])
			print author
			author = author[0] 
		except ObjectDoesNotExist:
			pass
		if author is not None:
			author = Author(
				last_name = a[0],
				fore_name = a[1],
				initials = a[2]
			)
			author.save()

			# Link author to affiliation
			if affiliation and not author.affiliations.filter(pk=affiliation.pk).exists():
				author.affiliations.add(affiliation)
			authors.append(author)
		

	# Publication Details
	pd = paper['publication_details']
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
	article = None
	try:
		article = Article.objects.get(pk=paper['pmid'])
	except ObjectDoesNotExist:
		try:
			article = Article(
				pmid = paper['pmid'],
				doi = paper['doi'],
				title = paper['title'],
				abstract = paper['abstract'],
				pub_type = paper['pub_type'],
				authors_list = paper['authors_list'],
				author_keywords = paper['author_keywords'],
				pub_details = pub_details
			)
			article.save()
		except Exception, e:
			print 'Error saving paper...'
			print_red(str(e))
			print paper
			return None

	# Link article to authors
	for a in authors:
		try:
			article.authors.add(a)
		except Exception, e:
			print 'Error adding author ' + a.fore_name + ' ' + a.last_name + ' to paper ' + str(article.pmid)
			print_red(str(e))
	return article



'''
Test fetching times without multiprocessing
'''
def fetch_test(base_url, query_key, web_env, retmax, count, cores):

	print 'eFetching ...'
	paper_count = 0
	tmsp = time.time()

	for i in range(count/retmax):
		retstart = i * retmax
		url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)

		resp = requests.get(url_fetch)
		soup = bs(resp.text.encode('utf-8'), 'xml')
		papers = soup.find_all('PubmedArticle')
		paper_count += len(papers)
		print 'Fetched ' + str(len(papers)) + ' papers --> retstart = ' + str(retstart) + ', retmax = ' + str(retmax)
	
	tmsp = time.time() - tmsp

	print_green('Total papers = ' + str(paper_count) + ', Time Lapse = ' + str(tmsp) + ' sec.')
	# print papers[0]
	# print type(papers[0])







