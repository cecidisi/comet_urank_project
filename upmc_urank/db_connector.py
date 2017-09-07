from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from conf_navigator.models import *
from upmc_urank.serializers import *
import json

class DBconnector:

	@classmethod
	def get_documents(cls):
		articles = Article.objects.all()[:500]
		articles = ArticleSerializer.setup_eager_loading(articles)
		articles =  ArticleSerializer(articles, many=True).data
		for a in articles:
			a['id'] = a['pmid']
		return articles

		# talks = TalkSerializer(talks, many=True).data
		# for idx, d in enumerate(talks):
		# 	d['keywords'] = json.loads(d['keywords_str']['keyword_str'])
		# return talks
	

	@classmethod
	def get_keywords(cls):
		keywords = PubmedGlobalKeyword.objects.all().order_by('df')
		return PubmedGlobalKeywordSerializer(keywords, many=True).data
		# Return after renaming colvideos as appears_in
		# keywords = [ dict(k, **{'appears_in' : k.pop('colvideos')}) for k in keywords]
		# return keywords

