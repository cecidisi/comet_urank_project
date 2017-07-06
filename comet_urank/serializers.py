# from django.forms import widgets
# from django.contrib.auth.models import User
from rest_framework import serializers
from comet_urank.models import *


class KeywordPosTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordPosTitle
        fields = ('from_pos', 'to_pos')


class KeywordPosDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordPosDetail
        fields = ('from_pos', 'to_pos')


class ColKeywordSerializer(serializers.ModelSerializer):
    positions_title = KeywordPosTitleSerializer(many=True, read_only=True)
    positions_detail = KeywordPosDetailSerializer(many=True, read_only=True)

    def setup_eager_loading(cls, queryset):
        queryset = queryset.prefetch_related('positions_title')
        queryset = queryset.prefetch_related('positions_detail')
        return queryset

    class Meta:
        model = ColKeyword
        fields = ('stem', 'tfidf', 'tf', 'score', 'positions_title', 'positions_detail')



class ColKeywordStrSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColKeywordStr
        fields = ('keyword_str',)


class UsertagSerializer(serializers.ModelSerializer):
    """ Uncomment to fill nested objects """
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # colvideos = ColvideoSerializer(read_only=True, many=True)

    class Meta:
        model = Usertag
        fields = ('id', 'tag', 'count', 'colvideos', 'proxusertags')
        # depth = 1


""" Takes usertags from usertag_colvideo table and returns only id and tag instead of full info """
class ColvideoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertag
        fields = ('tag',)


class ColvideoTagStrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColvideoTagStr
        fields = ('tag_str',) #'__all__'
        # fields = ('id','tag_str')


class ColvideoSerializer(serializers.ModelSerializer):
    # keywords = ColKeywordSerializer(many=True, read_only=True) # related_name should be set in FK definition
    # tags = ColvideoTagSerializer(read_only=True, many=True)
    keywords_str = ColKeywordStrSerializer(read_only=True)
    tags_str = ColvideoTagStrSerializer(read_only=True)
    
    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('keywords_str')
        queryset = queryset.prefetch_related('tags_str')
        # queryset = queryset.prefetch_related('keywords')
        # queryset = queryset.prefetch_related('tags')
        return queryset

    class Meta:
        model = Colvideo
        fields = ('id', 'title', 'detail', 'date', 'video_url', 'slide_url', 'paper_url', 'keywords_str', 'tags_str')
        # fields = ('id', 'title', 'detail', 'date', 'video_url', 'slide_url', 'paper_url', 'keywords', 'tags')
        

class KeyphraseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Keyphrase
        fields = '__all__'



class GlobalKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalKeyword
        fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'num_keyphrases')
        # fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'colvideos')







# Detail Chunk

class ColDetailChunkSerializer(serializers.ModelSerializer):
    # fcol = ColloquiumSerializer(read_only=True, many=True)

    class Meta:
        model = ColDetailChunk
        fields = ('id', 'sentence_original', 'sentence_parsed', 'pos', 'is_col_desc_man', 'is_col_desc_aut', 'fcol')





