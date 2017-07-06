# from django.forms import widgets
# from django.contrib.auth.models import User
from rest_framework import serializers
from conf_navigator.models import *


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class KwPosTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KwPosTitle
        fields = ('from_pos', 'to_pos')


class KwPosAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = KwPosAbstract
        fields = ('from_pos', 'to_pos')


class TalkKeyworderializer(serializers.ModelSerializer):
    positions_title = KwPosTitleSerializer(many=True, read_only=True)
    positions_detail = KwPosAbstractSerializer(many=True, read_only=True)

    def setup_eager_loading(cls, queryset):
        queryset = queryset.prefetch_related('positions_title')
        queryset = queryset.prefetch_related('positions_detail')
        return queryset

    class Meta:
        model = TalkKeyword
        fields = ('stem', 'tfidf', 'tf', 'score', 'positions_title', 'positions_detail')



class TalkKeywordStrSerializer(serializers.ModelSerializer):

    class Meta:
        model = TalkKeywordStr
        fields = ('keyword_str',)



class TalkSerializer(serializers.ModelSerializer):
    keywords_str = TalkKeywordStrSerializer(read_only=True)

    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('keywords_str')
        return queryset

    class Meta:
        model = Talk
        fields = ('id', 'title', 'abstract', 'content_type', 'author_list', 'keywords_str')
        # fields = ('id', 'title', 'abstract', 'content_type', 'author_list')



class TalkKeyphraseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TalkKeyphrase
        fields = '__all__'


class ConfGlobalKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfGlobalKeyword
        fields = ('id', 'stem', 'term', 'df', 'score', 'variations', 'num_keyphrases')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class SimUserNeighborSerializer(serializers.ModelSerializer):
    neighbor = UserSerializer()
    class Meta:
        model = SimUserNeighbor
        fields = ('neighbor', 'score')

class SimUserTalkSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = SimUserTalk
        fields = ('user_id', 'talk_id', 'score')



