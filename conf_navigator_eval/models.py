# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

from conf_navigator.models import User

'''
TABLES FOR EVALUATION ONLY
'''

class UserEval(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=400)
    username = models.CharField(max_length=400, null=True)
    email = models.TextField(default='')
    type = models.CharField(max_length=100, 
        choices=(('original', 'original'), ('added', 'added')),
        default='original'
    )

    class Meta:
        db_table = 'user_eval'

class LatinSquares(models.Model):
	id = models.IntegerField(primary_key=True) 
	sequence = models.TextField()

	class Meta:
		db_table = 'latin_squares'



class EvalSetting(models.Model):
	user = models.ForeignKey(UserEval, on_delete=models.CASCADE, default='', related_name='eval_settings')
	ltsq = models.ForeignKey(LatinSquares, on_delete=models.CASCADE, default='', related_name='eval_settings')
	date = models.DateField(blank=True, null=True, default=datetime.date.today)

	class Meta:
		db_table = 'eval_setting'



class Task(models.Model):
	number = models.IntegerField()
	user = models.ForeignKey(UserEval, on_delete=models.CASCADE, default='', related_name='tasks')
	settings = models.ForeignKey(EvalSetting, on_delete=models.CASCADE, default='', related_name='tasks')
	date = models.DateField(blank=True, null=True, default=datetime.date.today)
	time_taken = models.IntegerField()

	class Meta:
		db_table = 'task'



class LoggedAction(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE, default='', related_name='logged_actions')
	action = models.CharField(max_length=200)
	action_type = models.CharField(max_length=200, null=True)
	timestamp = models.IntegerField()
	pos = models.IntegerField()
	item_id = models.TextField(default='')
	desciption = models.TextField()

	class Meta:
		db_table = 'logged_action'


class BookmarkEval(models.Model):
	pos = models.IntegerField()
	rating = models.IntegerField()
	talk_id = models.IntegerField()
	talk_title = models.TextField()
	task = models.ForeignKey(Task, on_delete=models.CASCADE, default='', related_name = 'bookmarks_eval')
	# user = models.ForeignKey(UserEval, on_delete=models.CASCADE, default='', related_name='bookmarks_eval')
	
	class Meta:
		db_table = 'bookmark_eval'


class QuestionItem(models.Model):
	id = models.IntegerField(primary_key=True)
	text = models.TextField()
	min_label = models.CharField(max_length=200, default='')
	max_label = models.CharField(max_length=200, default='')

	class Meta:
		db_table = 'question_item'


class AnswerItem(models.Model):
	value = models.IntegerField()
	question = models.ForeignKey(QuestionItem, on_delete=models.CASCADE, default='', related_name='answers')
	user = models.ForeignKey(UserEval, on_delete=models.CASCADE, default='', related_name='answers')

	class Meta:
		db_table = 'answer_item'











