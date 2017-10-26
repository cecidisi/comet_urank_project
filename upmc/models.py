# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from django_mysql.models import JSONField
import jsonfield
import datetime
import json

# Create your models here.


class Affiliation(models.Model):
	name = models.TextField(default='')

	class Meta:
		db_table = 'affiliation'



class Author(models.Model):
	last_name = models.TextField()
	fore_name = models.TextField()
	initials = models.TextField()
	affiliations = models.ManyToManyField(Affiliation, default='', related_name='author')

	class Meta:
		db_table = 'author'


class PublicationDetails(models.Model):
	journal = models.TextField()
	abbr = models.TextField(null=True, default='')
	issn = models.CharField(max_length=200, null=True)
	volume = models.CharField(max_length=200, null=True)
	issue = models.CharField(max_length=200, null=True)
	date_str = models.CharField(max_length=200, null=True, default='')
	year = models.IntegerField(null=True, default=-1)

	class Meta:
		db_table = 'publication_details'


# class PubmedKeywordStr(models.Model):
#     keyword_str = models.TextField(blank=True, null=True)

#     class Meta:
#         db_table = 'pubmed_keyword_str'

class PubmedDocKeywords(models.Model):
	keywords = jsonfield.JSONField()
	pos_title = jsonfield.JSONField()
	pos_detail = jsonfield.JSONField()

	class Meta:
		db_table = 'pubmed_dockeywords'


class Article(models.Model):
	pmid = models.IntegerField(primary_key=True)
	doi = models.CharField(null=True, max_length=200)	
	title = models.TextField(default='')
	abstract  = models.TextField(default='')
	pub_type = models.CharField(max_length=100, default='', null=True)
	# year = models.IntegerField(null=True, default=-1)
	pub_details = models.OneToOneField(PublicationDetails, on_delete=models.CASCADE, null=True, default='', related_name='paper')
	authors_list = models.TextField(default='')
	authors = models.ManyToManyField(Author, default='', related_name='papers')
	author_keywords = models.TextField(default='', null=True)
	doc_keywords = models.OneToOneField(PubmedDocKeywords, on_delete=models.CASCADE, null=True, related_name='paper')

	class Meta:
		db_table = 'paper'



class PubmedTopic(models.Model):
	name = models.TextField()

	class Meta:
		db_table = 'pubmed_topic'


class PubmedGlobalKeyword(models.Model):
    stem = models.CharField(max_length=45, blank=True, null=True)
    term = models.CharField(max_length=45, blank=True, null=True)
    df = models.IntegerField(blank=True, null=True)
    entropy = models.FloatField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    variations = models.TextField()
    num_keyphrases = models.IntegerField(blank=True, null=True)
    # keyphrases = models.ManyToManyField(PubmedKeyphrase, blank=True, related_name='pubmed_global_keywords')
    # topic = models.ForeignKey(PubmedTopic, blank=True, on_delete=models.CASCADE, default='', related_name='pubmed_global_keywords')
    class Meta:
        db_table = 'pubmed_global_keyword'


class PubmedKeyphrase(models.Model):
    phrase = models.TextField()
    pos = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    stems = models.TextField()
    global_keyword = models.ForeignKey(PubmedGlobalKeyword, blank=True, on_delete=models.CASCADE, default='', related_name='keyphrases')

    class Meta:
        db_table = 'pubmed_keyphrase'



class PubmedYearFacet(models.Model):
	year = models.IntegerField()
	count = models.IntegerField()

	class Meta:
		db_table = 'pubmed_year_facet'






