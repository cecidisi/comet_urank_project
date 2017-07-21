# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.


class Affiliation(models.Model):
	name = models.TextField(default='')

	class Meta:
		db_table = 'affiliation'



class Author(models.Model):
	last_name = models.TextField(default='')
	fore_name = models.TextField(default='')
	initials = models.TextField(default='')
	affiliations = models.ManyToManyField(Affiliation, default='', related_name='author')

	class Meta:
		db_table = 'author'


class PublicationDetails(models.Model):
	journal = models.TextField()
	abbr = models.TextField(null=True, default='')
	issn = models.CharField(max_length=200, null=True)
	volume = models.CharField(max_length=20, null=True)
	issue = models.CharField(max_length=20, null=True)
	date_str = models.CharField(max_length=200, null=True, default='')
	year = models.IntegerField(null=True, default=-1)

	class Meta:
		db_table = 'publication_details'


class Article(models.Model):
	pmid = models.IntegerField(primary_key=True)
	doi = models.CharField(null=True, max_length=200)	
	title = models.TextField(default='')
	abstract  = models.TextField(default='')
	pub_type = models.CharField(max_length=100, default='', null=True)
	pub_details = models.OneToOneField(PublicationDetails, on_delete=models.CASCADE, null=True, default='', related_name='paper')
	authors = models.ManyToManyField(Author, default='', related_name='papers')
	author_keywords = models.TextField(default='', null=True)

	class Meta:
		db_table = 'paper'






