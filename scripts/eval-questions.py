from conf_navigator_eval.models import *


def run():
	questions = [
	'The system helped me to find interesting talks',
	'The system allowed me to easily refine my recommendations',
	'The system was intuitive',
	'The system was easy to control',
	'The system gave me a sense of transparency'
	]

	for idx, qtext in enumerate(questions):
		qitem = QuestionItem.objects.create(
			id = idx+1,
			text = qtext
		)
		print 'saved question --> ' + qitem.text
