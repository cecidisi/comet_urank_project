from conf_navigator_eval.models import *

def run():	
	EvalSetting.objects.all().delete()
	AnswerItem.objects.all().delete()
	FinalSurveyItem.objects.all().delete()
	BookmarkEval.objects.all().delete()
	LoggedAction.objects.all().delete()
	Task.objects.all().delete()