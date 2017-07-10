# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=400)
    begin_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    type = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'event'


class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=400)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=400, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default='', related_name='sessions')

    class Meta:
        db_table = 'session'


# Create your models here.
class Talk(models.Model):
    # id = contentID
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=400)
    abstract = models.TextField()
    content_type = models.CharField(max_length=200, null=True)
    author_list = models.TextField(null=True)
    address = models.TextField(null=True)
    # presentation info
    presentation_id = models.CharField(max_length=200, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    begin_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    #  foreign keys
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default='', related_name='talks')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default='', related_name='talks')

    class Meta:
        db_table = 'talk'


class User(models.Model):
    # id = userID
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=400)
    username = models.CharField(max_length=400, null=True)
    talks = models.ManyToManyField(Talk, blank=True, related_name='authors')
    bookmarks = models.ManyToManyField(Talk, blank=True, related_name='bookmarked_by')
    # # all_bookmarks = comma-separated ids of bookmarked talks, even if not in DB
    # all_bookmarks = models.TextField(default='')  
    type = models.CharField(max_length=100, 
        choices=(('original', 'original'), ('added', 'added')),
        default='original'
    )
    events = models.ManyToManyField(Event, blank=True, related_name='participants')

    class Meta:
        db_table = 'user'




class TalkKeywordStr(models.Model):
    keyword_str = models.TextField(blank=True, null=True)
    talk = models.OneToOneField(Talk, on_delete=models.CASCADE, default='', related_name='keywords_str')

    class Meta:
        db_table = 'talk_keyword_str'


#  Colloquium keywords
class TalkKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    tf = models.IntegerField(blank=True, null=True)
    tfidf = models.FloatField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    is_title = models.IntegerField(blank=True, null=True)
    pos_title = models.TextField(blank=True, null=True)
    pos_detail = models.TextField(blank=True, null=True)
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, default='', related_name='talk_keywords')
    
    class Meta:
        db_table = 'talk_keyword'


class KwPosTitle(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    talk_kw = models.ForeignKey(TalkKeyword, on_delete=models.CASCADE, default='', related_name='kw_positions_title')

    class Meta:
        db_table = 'kw_pos_title'


class KwPosAbstract(models.Model):
    from_pos = models.IntegerField(blank=True, null=True)
    to_pos = models.IntegerField(blank=True, null=True)
    talk_kw = models.ForeignKey(TalkKeyword, on_delete=models.CASCADE, default='', related_name='kw_positions_abstract')

    class Meta:
        db_table = 'kw_pos_abstract'


class TalkKeyphrase(models.Model):
    phrase = models.TextField()
    sequence = models.TextField()   # Parse as json later
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'talk_keyphrase'



class ConfGlobalKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    term = models.CharField(max_length=45, blank=True, null=True)
    df = models.IntegerField(blank=True, null=True)
    entropy = models.FloatField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    variations = models.TextField()
    num_keyphrases = models.IntegerField(blank=True, null=True)
    talk_keyphrases = models.ManyToManyField(TalkKeyphrase, blank=True, related_name='conf_global_keywords')
    event = models.ForeignKey(Event, blank=True, on_delete=models.CASCADE, default='', related_name='conf_global_keywords')
    class Meta:
        db_table = 'conf_global_keyword'


'''
    User for similarity computation
'''


class OldPaper(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=400)
    abstract = models.TextField()
    authorids = models.TextField(null=True)
    keyword_str = models.TextField(null=True)
    
    class Meta:
        db_table = 'old_paper'



class BookmarkSequence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='all_bookmarks')
    # all_bookmarks = comma-separated ids of bookmarked talks, even if not in DB
    all_bookmarks = models.TextField(default='') 

    class Meta:
        db_table = 'bookmark_sequence'



class SimUserNeighbor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name = 'sim_user_neighbors_u')
    neighbor = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='sim_user_neighbor_v')
    score = models.FloatField()
    pub_sim = models.FloatField(null=True)
    co_auth = models.FloatField(null=True)
    interest = models.FloatField(null=True)
    geo_dist= models.FloatField(null=True)
    soc_ctx = models.FloatField(null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default='', related_name='sim_user_neighbor')

    class Meta:
        db_table = 'sim_user_neighbor'



class SimUserTalk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='sim_user_talk')
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, default='', related_name='sim_user_talk')
    score = models.FloatField()

    class Meta:
        db_table = 'sim_user_talk'







