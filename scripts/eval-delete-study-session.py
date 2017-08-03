
from conf_navigator_eval.models import *
from conf_navigator.classes.bcolors import *


def run():
	user_id = 16
	try:
		user = UserEval.objects.get(pk=user_id)
		EvalSetting.objects.filter(user=user).delete()
		FinalSurveyItem.objects.filter(user=user).delete()
		print_green('Deleted session for ' + user.name)


	except Exception, e:
		print_red(str(e))
		exit

