# from django.forms import widgets
# from django.contrib.auth.models import User
from rest_framework import serializers
from upmc_urank.models import *




class PubmedKeywordStrSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedKeywordStr
        fields = ('keyword_str',)



class ArticleSerializer(serializers.ModelSerializer):
    keywords_str = PubmedKeywordStrSerializer(read_only=True)
    
    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('pub_details')
        queryset = queryset.prefetch_related('authors')
        queryset = queryset.prefetch_related('keywords_str')
        return queryset

    class Meta:
        model = Article
        fields = ('pmid', 'doi', 'title', 'abstract', 'pub_type', 'pub_details', 'authors', 'author_keywords', 'keywords_str')
   


# class KeyphraseSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = Keyphrase
#         fields = '__all__'



class PubmedGlobalKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubmedGlobalKeyword
        fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'num_keyphrases')



