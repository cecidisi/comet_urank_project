# from django.forms import widgets
# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import json



class PubmedKeywordStrSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedKeywordStr
        fields = ('keyword_str',)


class PublicationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationDetails
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pmid', read_only=True)
    year = serializers.IntegerField(source='pub_details.year', read_only=True)
    keywords = serializers.SerializerMethodField()

    def get_year(self, article):
        return article.pub_details.year

    def get_keywords(self, article):
        return json.loads(article.keywords_str.keyword_str)

    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('pub_details')
        queryset = queryset.prefetch_related('keywords_str')
        return queryset

    class Meta:
        model = Article
        fields = ('id', 'pmid', 'doi', 'title', 'pub_type', 'year', 'keywords')
   

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class ArticleFullSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pmid', read_only=True)
    pub_details = PublicationDetailsSerializer(read_only=True)
    authors = AuthorSerializer(read_only=True, many=True)
    # authors_list = AuthorSerializer(source='get_authors_list', read_only=True)
    authors_list = serializers.SerializerMethodField()

    def get_authors_list(self, article):
        _authors = Author.objects.filter(papers=article)
        return '; '.join([(a.last_name+', '+a.fore_name) for a in _authors]) if len(_authors) else ''

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.prefetch_related('pub_details')
        queryset = queryset.prefetch_related('authors')
        return queryset

    class Meta:
        model = Article
        fields = ('id', 'pmid', 'doi', 'title', 'abstract', 'pub_type', 'pub_details', 'authors', 'authors_list', 'author_keywords')


class KeyphraseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = PubmedKeyphrase
        fields = ('id', 'phrase', 'pos', 'count', 'stems', 'global_keyword_id')



class PubmedGlobalKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedGlobalKeyword
        fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'num_keyphrases')



