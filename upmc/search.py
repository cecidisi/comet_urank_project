from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Integer, Index, Search, Nested, Float, String, Object, Q
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from upmc.models import *
from helper.bcolors import *


# Create a connection to ElasticSearch
connections.create_connection()



# ElasticSearch "model" mapping out what fields to index
class ArticleIndex(DocType):
	id = Integer()
	doi = Text()
	title = Text()
	abstract = Text()
	pub_type = Text()
	year = Text()
	authors_list = Text()
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
			keywords = [k for k in a.doc_keywords.keywords.values()] or [],
			# pos_title = [{ 'stem': stem, 'from': p.from_pos, 'to': p.to_pos } for stem, p in a.doc_keywords.pos_title] or [],
			# pos_detail = [{ 'stem': stem, 'from': p.from_pos, 'to': p.to_pos } for stem, p in a.doc_keywords.pos_detail] or [],
			pos_title = [{ 'stem':stem, 'pos': val } for stem, val in a.doc_keywords.pos_title.iteritems()] or [],
			pos_detail = [{ 'stem':stem, 'pos': val } for stem, val in a.doc_keywords.pos_detail.iteritems()] or [],
			stems = a.doc_keywords.keywords.keys() or []
	    )
		obj.save()
		return obj.to_dict(include_meta=True)


	# Bulk indexing function, run in shell
	@classmethod
	def bulk_indexing(cls):
		from upmc.models import Article, PubmedDocKeywords, PublicationDetails
		eSearch.delete_index()
		articles = Article.objects.all().select_related('doc_keywords').select_related('pub_details')
		ArticleIndex.init()
		es = Elasticsearch()
		bulk(client=es, actions=(eSearch.index_article(d) for d in articles.iterator()))
		print_blue('Created index with ' + str(eSearch.count()) + ' documents (out of ' + str(len(articles)) + ')')


	@classmethod
	def count(cls):
		return Search(index='pubmed-article-index').count()


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



	@classmethod
	def search_by_keywords(cls, stems, keywords=False, text_positions = False):
		exclude_list = ['stems', 'abstract']
		if keywords == False:
			exclude_list.append('keywords')
		if text_positions == False:
			exclude_list = exclude_list + ['pos_title', 'pos_detail']
		q = Q('bool',
			should = [Q('match', stems=stem) for stem in stems],
			minimum_should_match = 1
		)
		s = Search(index='pubmed-article-index').query(q) \
			.source({ 'exclude': exclude_list})
		res = s[0:s.count()].execute()
		print 'eSearch returned ' + str(len(res)) + ' items'
		return [d.to_dict() for d in res]
		


	@classmethod
	def filter_by_ids(cls, ids_list):
		s = Search(index='pubmed-article-index')\
			.query('id', id=ids_list[0])
		return s.execute().to_dict()
		# return ArticleIndex.get(id=ids_list[0])



	@classmethod
	def search(cls, query=None):
		s = Search(index='pubmed-article-index')
		if query:
			s = s.filter('term', title=query)
		print 'Search found ' + str(s.count()) + ' results'
		response = s.execute()
		return response



	@classmethod
	def delete_index(cls):
		try:
			Index(name='pubmed-article-index').delete()
		except:
			print "Index doesn't exist"
