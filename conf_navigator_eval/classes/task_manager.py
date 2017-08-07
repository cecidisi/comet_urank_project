
from conf_navigator_eval.models import *
from conf_navigator_eval.serializers import *
from conf_navigator.classes.bcolors import *


class TaskManager:

	def __init__(self):
		self.user = None
		self.cur_task = 1
		

	def clear(self):
		self.cur_task = 1
		# self.user = None
		# self.ltsq = None # set in get_eval_setting_list()


	def get_last_task(self, user_id):
		user_tasks = Task.objects.filter(user_id=user_id).order_by('-id')
		if(len(user_tasks)):
			return user_tasks[0].number
		return 0
		

	def set_user(self, user_id):
		try: 
			user = UserEval.objects.get(pk = int(user_id))
			self.user = user
			print_blue('Set user in task mananager ID = ' + str(self.user.pk) + ' NAME = ' + self.user.name)
		except Exception, e:
			print_red('ERROR in set_user --> ' + user_id)
			print_red(str(e))


	def set_task(self, task_num):
		self.cur_task = task_num


	def get_eval_setting_list(self):
		# check if user already has settings assigned
		eval_settings = EvalSetting.objects.filter(user_id=self.user.id).select_related('ltsq').order_by('-id')
		if len(eval_settings):
			return eval_settings[0].ltsq.sequence.split(',')
				
		# Current user does not have Eval Settings yet
		# Fetch appropriate ltsq sequence and save eval_settings only once
		all_eval_settings = EvalSetting.objects.all().select_related('ltsq').order_by('-id')
		
		cur_ltsq_id = 1
		if len(all_eval_settings):
			last_eval_setting = all_eval_settings[0]
			print_red('Last used LTSQ id = ' + str(last_eval_setting.ltsq.id))
			last_ltsq_id = last_eval_setting.ltsq.id
			cur_ltsq_id = (last_ltsq_id + 1) if last_ltsq_id < 4 else 1
			print 'New cur_ltsq_id = ' + str(cur_ltsq_id)
			
		ltsq = LatinSquares.objects.get(pk=cur_ltsq_id)
		# save eval settings for current user
		eval_settings = EvalSetting(user = self.user, ltsq = ltsq)
		eval_settings.save()
		# Return LTSQ sequence for the user's eval setting
		print_blue('LTSQ sequence = ' + str(ltsq.sequence))
		return ltsq.sequence.split(',')

		# try:
		# 	eval_settings = EvalSetting.objects.select_related('ltsq').latest('id')
		# 	print_red('Last used LTSQ id = ' + str(eval_settings.ltsq_id))
		# 	last_ltsq_id = eval_settings.ltsq_id
		# 	cur_ltsq_id = (last_ltsq_id + 1) if last_ltsq_id < 4 else 1
		# 	print cur_ltsq_id
		# 	# self.
		# 	ltsq = LatinSquares.objects.get(pk=cur_ltsq_id)
		# except:
		# 	# self.
		# 	ltsq = LatinSquares.objects.get(pk=1)

		# print_blue('LTSQ sequence = ' + str(ltsq.sequence))
		# return ltsq.sequence.split(',')


	# receive ltsq.pk and user.pk
	def save_task(self, action_logs, bookmarks, elapsed_time):
		
		# fetch eval settings
		eval_settings = EvalSetting.objects.get(user=self.user)
		# try:
		# 	eval_settings = EvalSetting(user = self.user, ltsq = self.ltsq)
		# 	eval_settings.save()
		# except Exception, e:
		# 	print_red('ERROR saving Eval Setting --> ' +str(e))
		# 	print self.user
		# 	return None

		# save task
		try:
			task = Task(
				number = self.cur_task,
				user = self.user,
				settings = eval_settings,
				time_taken = int(elapsed_time)
			)
			task.save()
		except Exception, e:
			print_red('ERROR saving Task --> ' +str(e))
			return None
		
		# save logged actions
		for log in action_logs:
			try:
				action_log = LoggedAction(
					task = task,
					action = log['action'],
					# action_type = '',
					timestamp = log['timestamp'],
					pos = log['pos'],
					item_id = str(log['id']),
					description = log['description']
				)
				action_log.save()
			except Exception, e:
				print_red('ERROR saving LoggedAction --> ' +str(e))
				return None

		# save bookmarks eval
		for b in bookmarks:
			try:
				bm_eval = BookmarkEval(
					pos = b['pos'],
					rating = b['rating'],
					talk_id = b['id'],
					talk_title = b['title'],
					task = task
					# user = self.user
				)
				bm_eval.save()
				# Save to bookmarks_eval dict to mark talks bookmarked during the task
				# self.bookmarks_eval[bm_eval.talk_id] = bm_eval
			except Exception, e:
				print_red('ERROR saving BookmarkEval --> ' + str(e))
				return None

		return True



	def get_post_task_questions(self):
		questions = QuestionItem.objects.filter(type='post-task').order_by('num')
		return QuestionItemSerializer(questions, many=True).data


	# receive user.pk, task.pk and question.pk to link value to avoid keeping self.questions and self.task
	def save_post_task_questions(self, values):
		# fetch task, already saved in save_task()
		try:
			task = Task.objects.filter(user=self.user).filter(number=self.cur_task).order_by('-id')[0]
		except Exception, e:
			print_red('ERROR fetching task --> ' + str(e))
			return None

		for idx, item in enumerate(values):
			print item
			try: 
				answer = AnswerItem(
					value = int(item['val']),
					# question = self.questions[idx],
					question_id = int(item['qid']),
					task = task,
					user = self.user
				)
				answer.save()
				print 'Saved value = ' + str(answer.value) +' for question #'+ str(answer.question_id)
			except Exception, e:
				print_red('ERROR saving answers --> ' + str(e))
				return None
		return True


	def get_final_survey(self):
		final_questions = QuestionItem.objects.filter(type='post-study').order_by('num')
		return QuestionItemSerializer(final_questions, many=True).data


	# receive user.pk and array of { question.pk: choice }
	def save_final_survey(self, choices):
		for idx, item in enumerate(choices):
			try:
				survey_item = FinalSurveyItem(
					choice = item['val'],
					# question = self.final_questions[idx],
					question_id = int(item['qid']),
					user = self.user
				)
				survey_item.save()
				print 'Saved value = '+ str(survey_item.choice) + ' for final question: #'+ str(survey_item.question_id)
			except Exception, e:
				print_red('ERROR saving final survey --> ' + str(e))
				return None
		return True



	#  fetch from task.pk user.pk (indirect)
	def mark_bookmarked(self, talks):
		
		bookmarks_eval = {}
		tasks = Task.objects.filter(user=self.user).prefetch_related('bookmarks_eval')
		for task in tasks:
			for bm_eval in task.bookmarks_eval.all():
				bookmarks_eval[bm_eval.talk_id] = bm_eval

		for t in talks:
			t['is_bookmarked'] = True if t['id'] in bookmarks_eval else False
		return talks



	def filter_out_bookmarked(self, talks):
		bookmarks_eval = {}
		tasks = Task.objects.filter(user=self.user).prefetch_related('bookmarks_eval')
		for task in tasks:
			for bm_eval in task.bookmarks_eval.all():
				bookmarks_eval[bm_eval.talk_id] = bm_eval

		return [t for t in talks if t['id'] not in bookmarks_eval]
			
		



	def get_logged_actions(self):
		actions = LoggedAction.objects.all()
		actions = LoggedActionsSerializer(actions, many=True).data
		for a in actions:
			a['description'] = a['description'].encode('utf8')
		return actions


	def get_post_task_questionnaire_answers(self):
		questionnaires = AnswerItem.objects.all()
		return AnswerItemSerializer(questionnaires, many=True).data
		

	def get_final_survey_answers(self):
		surveys = FinalSurveyItem.objects.all()
		return FinalSurveySerializer(surveys, many=True).data


	def get_tasks_info(self):
		tasks = Task.objects.all()
		return TaskSerializer(tasks, many = True).data


	def get_bookmarks_eval(self):
		bookmarks = BookmarkEval.objects.all()
		return BookmarkEvalSerializer(bookmarks, many = True).data
			
