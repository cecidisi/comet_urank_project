from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Integer, Index, Search, Nested, Float, String, Q, A
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from upmc.models import *
from upmc.serializers import *
from helper.bcolors import *


# Create a connection to ElasticSearch
connections.create_connection()


class GlobalKeywordIndex(DocType):
	id = Integer()
	stem = Text()
	term = Text()
	score = Float()
	df = Integer()
	variations = String()
	num_keyphrases = Integer()
	phrases = Nested(
		properties = {
			'phrase': Text(),
		    'count': Integer(),
		    'stems': Text()
		}
	)
	class Meta:
		index = 'pubmed-global-keyword-index'



# ElasticSearch "model" mapping out what fields to index
class ArticleIndex(DocType):
	id = Integer()
	doi = Text()
	title = Text()
	abstract = Text()
	pub_type = Text()
	year = Text()
	authors_list = Text()
	pub_details = Nested(
		properties = {
			'journal': Text(),
			'issn': Text(),
			'volume': Text(),
			'issue': Text()
		}
	)
	# keywords = Text()
	keywords = Nested(
		properties = {
			'stem': Text(),
			'score': Float()
		}
	)
	pos_title = Nested(
		properties = {
			'stem': Text(),
			'pos': Nested(
				properties = {
					'from_pos': Integer(),
					'to_pos': Integer()
				}
			)
		}
	)
	pos_detail = Nested(
		properties = {
			'stem': Text(),
			'pos': Nested(
				properties = {
					'from_pos': Integer(),
					'to_pos': Integer()
				}
			)
		}
	)
	stems = Text()
	# keywords = Object(dynamic=True)

	class Meta:
		index = 'pubmed-article-index'


class eSearch():

	@classmethod
	def delete_index(cls, index_name):
		try:
			Index(name=index_name).delete()
		except:
			print "Index doesn't exist: " + index_name


	# Method for indexing the model
	@classmethod
	def index_article(cls, a):
		obj = ArticleIndex(
	        meta={ 'id': a.pmid },
	        id = a.pmid,
			doi = a.doi,
			title = a.title,
			abstract = a.abstract,
			pub_type = a.pub_type,
			year = a.pub_details.year,
			authors_list = a.authors_list,
			pub_details = PublicationDetailsSerializer(a.pub_details).data,
			keywords = [k for k in a.doc_keywords.keywords.values()] or [],
			# pos_title = [{ 'stem': stem, 'from': p.from_pos, 'to': p.to_pos } for stem, p in a.doc_keywords.pos_title] or [],
			# pos_detail = [{ 'stem': stem, 'from': p.from_pos, 'to': p.to_pos } for stem, p in a.doc_keywords.pos_detail] or [],
			pos_title = [{ 'stem':stem, 'pos': val } for stem, val in a.doc_keywords.pos_title.iteritems()] or [],
			pos_detail = [{ 'stem':stem, 'pos': val } for stem, val in a.doc_keywords.pos_detail.iteritems()] or [],
			stems = a.doc_keywords.keywords.keys() or []
	    )
		try:
			obj.save()
		except Exception, e:
			print_red(str(e))
		return obj.to_dict(include_meta=True)


	# Bulk indexing function, run in shell
	@classmethod
	def bulk_indexing_articles(cls):
		from upmc.models import Article, PubmedDocKeywords, PublicationDetails
		eSearch.delete_index('pubmed-article-index')
		articles = Article.objects.all().select_related('doc_keywords').select_related('pub_details')
		ArticleIndex.init()
		es = Elasticsearch()
		bulk(client=es, actions=(eSearch.index_article(d) for d in articles.iterator()))
		print_blue('eSearch: Created articles index with ' + str(Search(index='pubmed-article-index').count()) + ' documents (out of ' + str(len(articles)) + ')')


	@classmethod
	def create_year_aggregation(cls):
		s = Search(index='pubmed-article-index')
		# a = A('terms', field='year', size=0)
		# s.aggs.bucket('by_year', a)
		# s.aggs.bucket('by_year', 'terms', field='year')
		s.aggs.bucket('by_year', 'range', field='year'
			# , ranges = [
			# { 'to': 1990 },
			# { 'from': 1991, 'to': 2000 },
			# { 'from': 2001}
			# ]
		)	

		print_blue('eSearch: Created "year" aggregations')
		t = s.execute()

		return s.to_dict()


	# @classmethod
	# def get_year_facets(cls):
	# 	s = Search(index='pubmed-article-index')
	# 	s = s.execute()
	# 	print s.aggregations
	



	@classmethod
	def get_all_articles(cls):
		def serialize(d):
			# d = d.to_dict()
			try:
				# d['keywords'] = { k['stem']: k['score'] for k in d['keywords'] }
				d['keywords'] = { k['stem']: k for k in d['keywords'] }
			except Exception, e:
				d['keywords'] = {}
			return d			

		es = Elasticsearch()
		s = Search(using=es, index='pubmed-article-index').source({ 'exclude': ['abstract', 'stems']  })
		# print_green('Search found ' + str(s.count()) + ' results')
		res = s[0:s.count()].execute()
		print 'eSearch returned ' + str(len(res)) + ' items'
		res = [serialize(d) for d in res]
		# print res[0]
		return res

	@staticmethod
	def get_exclude_list(options):
		exclude_list = ['stems', 'abstract', 'pub_details', 'keywords', 'pos_title', 'pos_detail']
		for key, value in options.iteritems():
			if(value):
				try:
					exclude_list.remove(key)
				except ValueError:
					pass

		return exclude_list


	@staticmethod
	def filter_by_year_range(s, year_range):
		from_year = year_range[0]
		to_year = year_range[1]
		return s.filter('range', year={ 'from': from_year, 'to': to_year })


	@staticmethod
	def format_elem(d):
		d = d.to_dict()
		if 'keywords' in d:
			d['keywords'] = { k['stem']: k for k in d['keywords'] }
		if 'pos_title' in d:
			d['pos_title'] = { p['stem']: p['pos'] for p in d['pos_title'] }
		if 'pos_detail' in d:
			d['pos_detail'] = { p['stem']: p['pos'] for p in d['pos_detail'] }
		return d


	@classmethod
	def search_by_keywords(cls, stems, **options):

		q = Q('bool',
			should = [Q('match', stems=stem) for stem in stems],
			minimum_should_match = 1
		)
		s = Search(index='pubmed-article-index') \
			.query(q) \
			.source({ 'excludes': eSearch.get_exclude_list(options) })

		# Filter by year range
		if 'year_range' in options and len(options['year_range']):
			s = eSearch.filter_by_year_range(s, options['year_range'])

		offset = options['offset'] if 'offset' in options else 0
		count = options['count'] if 'count' in options else 1000
		res = s[offset:count].execute()
		print 'eSearch returned ' + str(len(res)) + ' items'
		return [eSearch.format_elem(d) for d in res]
		


	@classmethod
	def search_by_ids(cls, ids_list, **options):

		q = Q('bool',
			should = [Q('match', id=_id) for _id in ids_list],
			minimum_should_match = 1
		)
		s = Search(index='pubmed-article-index')\
			.query(q) \
			.source({ 
				'excludes': eSearch.get_exclude_list(options)
			})
		if 'year_range' in options and len(optons['year_range']):
			s = eSearch.filter_by_year_range(s, options['year_range'])
		offset = options['offset'] if 'offset' in options else 0
		res =  s[offset:len(ids_list)].execute()
		return [eSearch.format_elem(d) for d in res]



	# @classmethod
	# def get_text_positions(cls, ids_list, title=True, abstract=False):
	# 	include_list = ['id']
	# 	if title:
	# 		include_list.append('pos_title')
	# 	if abstract:
	# 		include_list.append('pos_detail')

	# 	def pos_to_dict(d):
	# 		d = d.to_dict()
	# 		if title and 'pos_title' in d:
	# 			d['pos_title'] = { p['stem']: p['pos'] for p in d['pos_title'] }
	# 		if abstract and 'pos_detail' in d:
	# 			d['pos_detail'] = { p['stem']: p['pos'] for p in d['pos_detail'] }
	# 		return d

	# 	q = Q('bool',
	# 		should = [Q('match', id=_id) for _id in ids_list],
	# 		minimum_should_match = 1
	# 	)
	# 	s = Search(index='pubmed-article-index')\
	# 		.query(q) \
	# 		.source({ 
	# 			'includes': include_list
	# 		})
	# 	res =  s[0:len(ids_list)].execute()
	# 	return [pos_to_dict(d) for d in res]
	# 	# return ArticleIndex.get(id=ids_list[0])


	'''
		GlobalKeywords Index
	'''

	# Method for indexing the model
	@classmethod
	def index_keyword(cls, k):
		obj = GlobalKeywordIndex(
	        meta={ 'id': k.id },
	        id = k.id,
			stem = k.stem,
    		term = k.term,
    		score = k.score,
    		df = k.df,
    		variations = k.variations,
    		num_keyphrases = k.num_keyphrases,
    		phrases = [{ 'phrase': p.phrase, 'count': p.count, 'stems': p.stems } for p in k.keyphrases.all()]
	    )
		try:
			obj.save()
		except Exception, e:
			print_red(str(e))
		return obj.to_dict(include_meta=True)


	# Bulk indexing function, run in shell
	@classmethod
	def bulk_indexing_keywords(cls):
		from upmc.models import PubmedGlobalKeyword, PubmedKeyphrase
		eSearch.delete_index('pubmed-global-keyword-index')
		keywords = PubmedGlobalKeyword.objects.prefetch_related('keyphrases').all()
		# print keywords[0].keyphrases
		
		GlobalKeywordIndex.init()
		es = Elasticsearch()
		bulk(client=es, actions=(eSearch.index_keyword(k) for k in keywords.iterator()))
		print_blue('eSearch: Created keywords index with ' + str(Search(index='pubmed-global-keyword-index').count()) + ' keywords (out of ' + str(len(keywords)) + ')')



	@classmethod
	def get_global_keywords(cls, num_keywords):
		es = Elasticsearch()
		s = Search(using=es, index='pubmed-global-keyword-index').sort('-score')
		res = s[0:num_keywords].execute()
		print 'eSearch: returned ' + str(len(res)) + ' keywords'
		res = [k.to_dict() for k in res]
		# print res[0]
		return res


