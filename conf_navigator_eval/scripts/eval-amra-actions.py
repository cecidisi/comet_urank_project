from conf_navigator_eval.models import *


def run():
	user_id = 100004961
	# user = UserEval.objects.get(pk=user_id)

	logs = {
		1 : [
			{ 'action': 'tag selected', 'description': 'neighbor-Judith Masthoff', 'tmsp': 57000 }
		],
		2 : [
			{ 'action': 'tag selected', 'description': 'keyword-user', 'tmsp': 38000 },
			{ 'action': 'tag selected', 'description': 'keyword-model', 'tmsp': 41000 },
			{ 'action': 'tag selected', 'description': 'keyword-data', 'tmsp': 47000 },
			{ 'action': 'tag selected', 'description': 'keyword-study', 'tmsp': 49000 }
		],
		3 : [
			{ 'action': 'tag selected', 'description': 'keyword-experiment', 'tmsp': 26000 },
			{ 'action': 'tag selected', 'description': 'keyword-personalization', 'tmsp': 29000 },
			{ 'action': 'tag selected', 'description': 'keyword-user', 'tmsp': 34000 },
			{ 'action': 'tag selected', 'description': 'keyword-model', 'tmsp': 36000 },
			{ 'action': 'tag deleted', 'description': 'keyword-experiment', 'tmsp': 101000 }
		],
		4 : [
			{ 'action': 'tag selected', 'description': 'keyword-prediction', 'tmsp': 65000 },
			{ 'action': 'tag selected', 'description': 'keyword-network', 'tmsp': 69000 },
			{ 'action': 'tag selected', 'description': 'keyword-analytics', 'tmsp': 103000 },
			{ 'action': 'tag selected', 'description': 'keyword-behavior', 'tmsp': 144000 },
			{ 'action': 'tag selected', 'description': 'keyword-relationship', 'tmsp': 237000 },
			{ 'action': 'tag selected', 'description': 'keyword-user', 'tmsp': 363000 },
			{ 'action': 'tag selected', 'description': 'keyword-model', 'tmsp': 364000 },
		]

	}
	
	for task in Task.objects.filter(user_id = user_id):
		print '======== Task #' + str(task.number)
		for log in logs[task.number]:
			logged_action = LoggedAction(
				action = log['action'],
				timestamp = log['tmsp'],
				pos = -1,
				item_id = -1,
				description = log['description'],
				task = task
			)
			logged_action.save()
			print 'Saved action = ' + logged_action.action + ' --> ' + logged_action.description






