from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from helper.bcolors import *
from upmc.search import *
from .models import *
from .serializers import UpmcUserSerializer
from .db_connector import *



class TaskManager:

	# @classmethod
	# def get_user(cls, username):
	# 	try:
	# 		user = UpmcUser.objects.get(username=username)
	# 		return UpmcUserSerializer(user).data
	# 	except ObjectDoesNotExist:
	# 		return False


	@staticmethod
	def get_user_by_id(user_id):
		try:
			return UpmcUser.objects.get(pk=user_id)
		except ObjectDoesNotExist:
			print_red('User with id = ' + str(user_id) + ' doesn\'t exist')
			return False



	@classmethod
	def bookmark(cls, params):
		user = TaskManager.get_user_by_id(params['user_id'])
		if not user:
			return False
		# Bookmark if not exist
		try:
			UpmcBookmark.objects.get(
				item_id = int(params['item_id']),
				item_title = params['item_title'],
				pos = int(params['pos']),
				upmc_user_id = user.id
			)
			print 'Bookmark already exists, not saving again'
			return True
		except ObjectDoesNotExist:
			# Made sure it doesn't exist, can save now
			bm = UpmcBookmark(
				item_id = int(params['item_id']),
				item_title = params['item_title'],
				pos = int(params['pos']),
				upmc_user = user
			)
			bm.save()
			print 'Saved bookmark for username='+str(user.username)
			return True
		except Exception, e:
			print 'Error saving bookmark'
			print_red(str(e))
			return False


	@classmethod
	def unbookmark(cls, params):
		user_id = params['user_id']
		item_id = params['item_id']
		try:
			UpmcBookmark.objects.filter(upmc_user_id=user_id).filter(item_id=item_id).delete()
		except Exception:
			print 'No bookmark to delete'

		return True


	@classmethod
	def save_task(cls, params):
		user = TaskManager.get_user_by_id(params['user_id'])
		if not user:
			return False
		# Save task
		task = None
		try:
			task = UpmcTask(
				elapsed_time = params['elapsed_time'],
				upmc_user = user,
				tool = 'urank'
			)
			task.save()
			print 'Saved task for user = ' + str(user.username)
		except IntegrityError, e:
			task = UpmcTask.objects.get(upmc_user=user)
			print 'Task for ' + user.username + ' already exist'

		# Save action logs
		action_logs = params['action_logs']
		for l in action_logs:
			try:
				action_log = UpmcActionLog(
					action = l['action'],
					timestamp = l['timestamp'],
					item_id = l['item_id'],
					item_name = l['item_name'],
					pos = l['pos'],
					upmc_user = user
				)
				action_log.save()
			except ValueError, e:
				print_red('Error saving action log')
				print e
		print 'Saved ' + str(len(action_logs)) + ' action logs for user = ' + str(user.username)

		time_logs = params['time_logs']
		for l in time_logs:
			try:
				time_log =  UpmcTimeLog(
					timestamp = l['timestamp'],
					duration = l['duration'],
					item_id = l['item_id'],
					item_name = l['item_name'],
					pos = l['pos'],
					upmc_user = user
				)
				time_log.save()
			except ValueError, e:
				print_red('Error saving time log')
				print e
		print 'Saved ' + str(len(time_logs)) + ' time logs for user = ' + str(user.username)
		return True



	@classmethod
	def mark_bookmarked(cls, articles, bookmarks):
		item_ids = [b['item_id'] for b in bookmarks]
		for d in articles:
			d['bookmarked'] = True if d['id'] in item_ids else False
		return articles



	@classmethod
	def get_bookmarks(cls, user_id=None):
		if not user_id or user_id is None:
			return None

		bookmarks = DBconnector.get_bookmarks(user_id)
		ids = [b['item_id'] for b in bookmarks]
		bookmarks = eSearch.search_by_ids(ids, abstract=True, pub_details=True)
		# Flatten publication details
		for b in bookmarks:
			# b['title'] = b['title'].encode("utf-8")
			# b['abstract'] = b['abstract'].encode("utf-8")
			for field, value in b['pub_details'].iteritems():
				b[field] = value
			b.pop('pub_details', None)

		return bookmarks


	@classmethod
	def save_pubmed_task(cls, params):
		user = TaskManager.get_user_by_id(params['user_id'])
		if not user:
			return False

		# Save task
		task = None
		try:
			task = UpmcTask(
				elapsed_time = params['elapsed_time'],
				upmc_user = user,
				tool = 'pubmed'
			)
			task.save()
			print 'Saved pubmed task for user = ' + str(user.username)
		except IntegrityError, e:
			task = UpmcTask.objects.get(upmc_user=user)
			print 'Task for ' + user.username + ' already exist'
		return True






