from rest_framework import serializers
from conf_navigator_eval.models import *


class LatinSquaresSerializer(serializers.ModelSerializer):
	class Meta:
		model = LatinSquares
		fields = '__all__'


class EvalSettingSerializer(serializers.ModelSerializer):
	ltsq = LatinSquaresSerializer(read_only=True)
	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('ltsq')
		return queryset

	class Meta:
		model = EvalSetting
		fields = ('id', 'date', 'ltsq')


class QuestionItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionItem
		fields = '__all__'


class UserEvalSerializer(serializers.ModelSerializer):
	class Meta:
		model= UserEval
		fields = ('id', 'name')



class TaskSerializer(serializers.ModelSerializer):
	user_id = serializers.CharField(source='user.pk', read_only=True)
	user_name = serializers.CharField(source='user.name', read_only=True)
	ltsq_seq = serializers.CharField(source='settings.ltsq.sequence', read_only=True)
	condition = serializers.SerializerMethodField()
	
	def get_condition(self, task):
		condition =  task.settings.ltsq.sequence.split(',')[task.number-1]
		return condition

	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('user')
		queryset = queryset.prefetch_related('settings')
		return queryset

	class Meta:
		model = Task
		fields = ('user_id', 'user_name', 'number', 'ltsq_seq', 'condition', 'date', 'time_taken')




class LoggedActionsSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source='task.user.pk', read_only=True)
	user_name = serializers.CharField(source='task.user.name', read_only=True)
	task_num = serializers.IntegerField(source='task.number', read_only=True)
	date = serializers.CharField(source='task.date', read_only=True)
	condition = serializers.SerializerMethodField()

	def get_condition(self, action):
		condition =  action.task.settings.ltsq.sequence.split(',')[action.task.number-1]
		return condition

	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('task')
		return queryset

	class Meta:
		model = LoggedAction
		fields = ('user_id', 'user_name', 'date', 'condition', 'task_num', 'action', 'action_type', 'timestamp', 'pos', 'description', 'item_id')



class AnswerItemSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source='user.pk', read_only=True)
	user_name = serializers.CharField(source='user.name', read_only=True)
	task_num = serializers.IntegerField(source='task.number', read_only=True)
	condition = serializers.SerializerMethodField()
	q_num = serializers.SerializerMethodField()
	question = serializers.SerializerMethodField()

	def get_condition(self, item):
		condition =  item.task.settings.ltsq.sequence.split(',')[item.task.number-1]
		return condition

	def get_q_num(self, item):
		return item.question.num

	def get_question(self, item):
		return item.question.text

	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('user')
		queryset = queryset.prefetch_related('question')
		queryset = queryset.prefetch_related('task')

	class Meta:
		model = AnswerItem
		fields = ('user_id', 'user_name', 'task_num', 'condition', 'q_num', 'question', 'value')


class FinalSurveySerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source='user.pk', read_only=True)
	user_name = serializers.CharField(source='user.name', read_only=True)
	q_num = serializers.SerializerMethodField()
	question = serializers.SerializerMethodField()

	def get_q_num(self, item):
		return item.question.num

	def get_question(self, item):
		return item.question.text

	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('user')
		queryset = queryset.prefetch_related('question')

	class Meta:
		model = FinalSurveyItem
		fields = ('user_id', 'user_name', 'q_num', 'question', 'choice')


