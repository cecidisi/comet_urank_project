# from django.forms import widgets
# from django.contrib.auth.models import User
from rest_framework import serializers
from upmc_urank.models import *
import json



class PubmedKeywordStrSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedKeywordStr
        fields = ('keyword_str',)



class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    # keywords_str = PubmedKeywordStrSerializer(read_only=True)
    keywords = serializers.SerializerMethodField()

    def get_id(self, article):
        return article.pmid

    def get_keywords(self, article):
        return json.loads(article.keywords_str.keyword_str)

    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        # queryset = queryset.prefetch_related('pub_details')
        # queryset = queryset.prefetch_related('authors')
        queryset = queryset.prefetch_related('keywords_str')
        return queryset

    class Meta:
        model = Article
        fields = ('id', 'pmid', 'doi', 'title', 'pub_type', 'keywords')
   


class ArticleFullSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, article):
        return article.pmid

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.prefetch_related('pub_details')
        queryset = queryset.prefetch_related('authors')
        return queryset

    class Meta:
        model = Article
        fields = ('id', 'pmid', 'doi', 'title', 'abstract', 'pub_type', 'pub_details', 'authors', 'author_keywords')


class KeyphraseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = PubmedKeyphrase
        fields = ('id', 'phrase', 'pos', 'count', 'stems', 'global_keyword_id')



class PubmedGlobalKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedGlobalKeyword
        fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'num_keyphrases')



