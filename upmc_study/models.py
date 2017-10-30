# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models

# Create your models here.


class UpmcUser(models.Model):
	first_name = models.CharField(max_length=400)
	last_name = models.CharField(max_length=400)
	username = models.CharField(max_length=400)

	class Meta:
		db_table = 'upmc_user'


class UpmcActionLog(models.Model):
	action = models.CharField(max_length=200)
	timestamp = models.IntegerField()
	item_id = models.TextField(default='', null=True)
	item_name = models.TextField(default='', null=True)
	pos = models.IntegerField(null=True)
	value = models.CharField(null=True, default='', max_length=100)
	upmc_user = models.ForeignKey(UpmcUser, null=True)

	class Meta:
		db_table = 'upmc_action_log'


class UpmcTimeLog(models.Model):
	item_id = models.TextField(default='', null=True)
	item_name = models.TextField(default='', null=True)
	pos = models.IntegerField(null=True)
	timestamp = models.IntegerField()
	duration = models.IntegerField()
	upmc_user = models.ForeignKey(UpmcUser, null=True)

	class Meta:
		db_table = 'upmc_time_log'




class UpmcBookmark(models.Model):
	item_id = models.IntegerField()
	item_title = models.TextField()
	pos = models.IntegerField()
	upmc_user = models.ForeignKey(UpmcUser, on_delete=models.CASCADE, default='', related_name='bookmarks')
	
	class Meta:
		db_table = 'upmc_bookmark'



class UpmcTask(models.Model):
	date_completed = models.DateField(blank=True, null=True, default=datetime.date.today)
	elapsed_time = models.IntegerField()
	tool = models.TextField(default='')
	upmc_user = models.OneToOneField(UpmcUser, related_name='task')

	class Meta:
		db_table = 'upmc_task'


