from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
# from conf_navigator.models import *
from .models import *
from .serializers import *
from helper.bcolors import *
import json

class DBconnector:

	@classmethod
	def get_articles(cls):
		articles = Article.objects.all()
		articles = ArticleSerializer.setup_eager_loading(articles)
		return ArticleSerializer(articles, many=True).data


	@classmethod
	def get_keywords(cls):
		keywords = PubmedGlobalKeyword.objects.all().order_by('-score')
		return PubmedGlobalKeywordSerializer(keywords, many=True).data


	@classmethod
	def get_article_details(cls, doc_id):
		article = Article.objects.get(pk = doc_id)
		return ArticleFullSerializer(article).data


	@classmethod
	def get_keyphrases(cls, kw_id):
		keyphrases = PubmedKeyphrase.objects.filter(global_keyword_id = kw_id)
		return KeyphraseSerilizer(keyphrases, many=True).data


	@classmethod
	def search_features(cls, feature_type, text):
		if feature_type == 'keyword':
			keywords = PubmedGlobalKeyword.objects.filter(term__contains=text)
			print_blue(str(len(keywords)))
			if len(keywords):
				return PubmedGlobalKeywordSerializer(keywords, many=True).data
		return []




