
from conf_navigator_eval.models import *
from conf_navigator_eval.serializers import *
from conf_navigator.classes.bcolors import *


class TaskManager:

	def __init__(self):
		self.user = None
		self.ltsq = None
		self.task = None
		self.cur_task = 1
		self.questions = []
		self.bookmarks_eval = {}
		self.final_questions = []

	def clear(self):
		self.cur_task = 1
		# self.user = None
		# self.ltsq = None # set in get_eval_setting_list()


	def set_user(self, user_id):
		try: 
			user = UserEval.objects.get(pk = int(user_id))
			self.user = user
			print_blue('Set user in task mananager ID = ' + str(self.user.pk) + ' NAME = ' + self.user.name)
		except Exception, e:
			print_red('ERROR in set_user --> ' + user_id)
			print_red(str(e))



	def next_task(self):
		self.cur_task += 1



	def get_eval_setting_list(self):
		self.ltsq = None
		try:
			eval_settings = EvalSetting.objects.latest('id')
			print_red(str(eval_settings.ltsq_id))
			last_ltsq_id = eval_settings.ltsq_id
			cur_ltsq_id = (last_ltsq_id + 1) if last_ltsq_id < 4 else 1
			print cur_ltsq_id
			self.ltsq = LatinSquares.objects.get(pk=cur_ltsq_id)
		except:
			self.ltsq = LatinSquares.objects.get(pk=1)

		print_blue('LTSQ sequence = ' + str(self.ltsq.sequence))
		return self.ltsq.sequence.split(',')



	def save_task(self, params):
		action_logs = params['action_logs']
		bookmarks = params['bookmarks']
		elapsed_time = params['elapsed_time']
		
		# save eval settings
		print 'ABOUT TO SAVE EVAL SETTINGS'
		print self.ltsq.pk
		print self.ltsq.sequence
		try:
			eval_settings = EvalSetting(user = self.user, ltsq = self.ltsq)
			eval_settings.save()
		except Exception, e:
			print_red('ERROR saving Eval Setting --> ' +str(e))
			print self.user
			return None

		# save task
		try:
			self.task = Task(
				number = self.cur_task,
				user = self.user,
				settings = eval_settings,
				time_taken = int(elapsed_time)
			)
			self.task.save()
		except Exception, e:
			print_red('ERROR saving Task --> ' +str(e))
			return None
		
		# save logged actions
		for log in action_logs:
			try:
				action_log = LoggedAction(
					task = self.task,
					action = log['action'],
					# action_type = '',
					timestamp = log['timestamp'],
					pos = log['pos'],
					item_id = str(log['id']),
					desciption = log['description']
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
					task = self.task
					# user = self.user
				)
				bm_eval.save()
				# Save to bookmarks_eval dict to mark talks bookmarked during the task
				self.bookmarks_eval[bm_eval.talk_id] = bm_eval
			except Exception, e:
				print_red('ERROR saving BookmarkEval --> ' + str(e))
				return None

		return True



	def get_post_task_questions(self):
		self.questions = QuestionItem.objects.filter(type='post-task').order_by('num')
		return QuestionItemSerializer(self.questions, many=True).data



	def save_post_task_questions(self, values):
		for idx, val in enumerate(values):
			try: 
				answer = AnswerItem(
					value = int(val),
					question = self.questions[idx],
					task = self.task,
					user = self.user
				)
				answer.save()
				print 'Saved value = ' + str(answer.value) +' for question '+ self.questions[idx].text
			except Exception, e:
				print_red('ERROR saving answers --> ' + str(e))
				return None
		return True


	def get_final_survey(self):
		self.final_questions = QuestionItem.objects.filter(type='post-study').order_by('num')
		return QuestionItemSerializer(self.final_questions, many=True).data



	def save_final_survey(self, choices):
		for idx, choice in enumerate(choices):
			try:
				survey_item = FinalSurveyItem(
					choice = choice,
					question = self.final_questions[idx],
					user = self.user
				)
				survey_item.save()
				print 'Saved value = '+ str(survey_item.choice) + ' for final question: '+ self.final_questions[idx].text
			except Exception, e:
				print_red('ERROR saving final survey --> ' + str(e))
				return None
		return True



	def mark_bookmarked(self, talks):
		for t in talks:
			t['is_bookmarked'] = True if t['id'] in self.bookmarks_eval else False
		return talks


	def filter_out_bookmarked(self, talks):
		return [t for t in talks if t['id'] not in self.bookmarks_eval]
			
		






			
