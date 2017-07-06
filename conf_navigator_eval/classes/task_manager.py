
from conf_navigator_eval.models import *
from conf_navigator_eval.serializers import *
from conf_navigator.classes.bcolors import *


class TaskManager:

	def __init__(self):
		self.user = None
		self.ltsq = None
		self.cur_task = 1

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
			print_red('ERROR --> ' +str(e))



	def next_task(self):
		self.cur_task += 1



	def get_eval_setting_list(self):
		self.ltsq = None
		eval_settings = EvalSetting.objects.latest('id')
		if eval_settings:
			last_ltsq_id = eval_settings.ltsq_id
			cur_ltsq_id = (last_ltsq_id + 1) % 4
			print cur_ltsq_id
			self.ltsq = LatinSquares.objects.get(pk=cur_ltsq_id)
		else:
			self.ltsq = LatinSquares.objects.get(pk=1)

		print_blue('LTSQ sequence = ' + str(self.ltsq.sequence))
		return self.ltsq.sequence.split(',')



	def save_task(self, params):
		action_logs = params['action_logs']
		elapsed_time = params['elapsed_time']
		
		# save eval settings
		print 'ABOUT TO SAVE EVAL SETTINGS'
		print self.ltsq.pk
		print self.ltsq.sequence
		try:
			eval_settings = EvalSetting(user = self.user, ltsq = self.ltsq)
			eval_settings.save()
		except Exception, e:
			print_red('ERROR --> ' +str(e))
			return None

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
			print_red('ERROR --> ' +str(e))
			return None
		
		# saved logged actions
		for log in action_logs:
			try:
				action_log = LoggedAction(
					task = task,
					action = log['action'],
					# action_type = '',
					timestamp = log['timestamp'],
					pos = log['pos'],
					item_id = str(log['id']),
					desciption = log['description']
				)
				action_log.save()
			except Exception, e:
				print_red('ERROR --> ' +str(e))
				return None

		return True


			
