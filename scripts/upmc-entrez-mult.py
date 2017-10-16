# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import urllib2
import requests
import unicodedata
import datetime
import time
import multiprocessing as mp
from django import db
from progressbar import *
from itertools import chain
from bs4 import BeautifulSoup as bs
from functools import partial
from conf_navigator.classes.bcolors import *
from upmc_urank.models import *


def run():
	print 'RUN'
	start = time.time()
	clean_db()
	term = 'migraine'
	count = 1000 # Total number of items
	retmax = 100	# Number items per batch
	cores = max(10, int(mp.cpu_count() *.75))
	base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	query_key, web_env, max_count = search(base_url, term)
	count = min(count, max_count) if count else max_count
	# fetch_test(base_url, query_key, web_env, retmax, count, cores)
	fetch_parallel(base_url, query_key, web_env, retmax, count, cores)
	print_blue('Total Time Elapsed = ' + secToMMSS(time.time() - start))


def clean_db():
	Affiliation.objects.all().delete()
	Author.objects.all().delete()
	PublicationDetails.objects.all().delete()
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
	



def fetch_worker(base_url, query_key, web_env, retmax, batches, i):
	retstart = i * retmax
	url_fetch = base_url + 'efetch.fcgi?db=pubmed&rettype=abstract&query_key=' + query_key + '&WebEnv=' + web_env + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)
	max_attempts = 3
	cur_attempt = 1
	items = []
	while(cur_attempt <= max_attempts and len(items) == 0):
		resp = requests.get(url_fetch)
		soup = bs(resp.text.encode('utf-8'), 'xml')
		items = soup.find_all('PubmedArticle')
		cur_attempt += 1
	print 'Batch (' + str(i+1) + '/' + str(batches) + ') --> Fetched ' + str(len(items)) + ' items ('+str(cur_attempt-1)+' attempt/s) [retstart = ' + str(retstart) + ', retmax = ' + str(retmax) +']'
	paper_count = 0
	# articles = []
	for p in items:
		paper = save_paper(parse_paper(p))
		if paper:
			# articles.append(paper)
			paper_count += 1
	print 'Batch (' + str(i+1) + '/' + str(batches) + ') --> Saved ' +str(paper_count)+ ' items'
	return paper_count
	# return articles



def fetch_parallel(base_url, query_key, web_env, retmax, count, cores):
	print 'eFetching with ' +str(cores)+ ' processes ...'
	batches = count/retmax
	jobs = []
	db.connections.close_all()
	tmsp1 = time.time()

	worker = partial(fetch_worker, base_url, query_key, web_env, retmax, batches)
	pool = mp.Pool(processes = cores)
	jobs = pool.map(worker, range(batches))
	pool.close()
	pool.join()


	from functools import reduce
	tmsp2 = time.time() - tmsp1
	paper_count = str(reduce((lambda x, y: x+y), jobs))
	# # jobs is list of lists
	# papers = list(chain.from_iterable(jobs))
	# paper_count = str(len(papers))
	
	print_green('Total papers =  ' + paper_count + '; eFetch Time = ' + secToMMSS(tmsp2))


	# # Set progressbar
	# widgets = ['Saving papers: ', Percentage(), ' ', Bar(marker='*',left='[',right=']'), ' ', ETA()]
	# pbar = ProgressBar(widgets=widgets, maxval=len(papers))
	# pbar.start()

	# saved_papers = 0
	# for i, d in enumerate(papers):
	# 	if save_paper(d):
	# 		saved_papers += 1
	# 	pbar.update(i)

	# pbar.finish()
	# tmsp3 = time.time() - tmsp1
	# print_green('Saved ' +str(saved_papers)+ ' papers. Total time elapsed --> ' + '{}:{}'.format(*divmod(int(tmsp3), 60)))

def secToMMSS(sec):
	return ':'.join([(str(i) if len(str(i))>1 else '0'+str(i)) for i in  divmod(int(sec), 60)])
	

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
			label = chunk.get('Label') or ''
			if label:
				paper['abstract'] += label + ': '
			paper['abstract'] += chunk.get_text() + '\n'
		paper['abstract'] = paper['abstract'][:-1]
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
	try:
		article = Article.objects.create(
			pmid = paper['pmid'],
			doi = paper['doi'],
			title = paper['title'],
			abstract = paper['abstract'],
			pub_type = paper['pub_type'],
			pub_details = pub_details,
			author_keywords = paper['author_keywords']
		)
		# Link article to authors
		for a in authors:
			article.authors.add(a)
		# print 'Saved article pmid = ' + str(article.pmid)
		return article
	except Exception, e:
		print_red(str(e))
		return None

	
	# print 'Saved ' + str(len(papers)) + ' articles'




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







