from conf_navigator_eval.models import *


def run():
	questions = [
	# NASA TLX
	{
		'text': 'How mentally demanding was the task?', 'min_label': 'Very Low', 'max_label': 'Very high'
	}, {
		'text': 'How physically demanding was the task?', 'min_label': 'Very Low', 'max_label': 'Very high'
	}, {
		'text': 'How hurried or rushed was the pace of the task?', 'min_label': 'Very Low', 'max_label': 'Very high'
	}, {
		'text': 'How successful were you in accomplishing what you were asked to do?', 'min_label': 'Perfect', 'max_label': 'Failure'
	}, {
		'text': 'How hard did you have to work to accomplish your level of performance?', 'min_label': 'Very Low', 'max_label': 'Very high'
	}, {
		'text': 'How insecure, discouraged, irritated, stressed, and annoyed were you?', 'min_label': 'Very Low', 'max_label': 'Very high'
	}, 
	# Custom questions
	{
		'text': 'The system helped me to find interesting papers', 'min_label': 'Strongly Disagree', 'max_label': 'Strongly Agree'
	}, {
		'text': 'The system allowed me to easily refine my recommendations', 'min_label': 'Strongly Disagree', 'max_label': 'Strongly Agree'
	}, {
		'text': 'The system was intuitive', 'min_label': 'Strongly Disagree', 'max_label': 'Strongly Agree'
	}, {
		'text': 'The system was easy to control', 'min_label': 'Strongly Disagree', 'max_label': 'Strongly Agree'
	}, {
		'text': 'The system gave me a sense of transparency', 'min_label': 'Strongly Disagree', 'max_label': 'Strongly Agree'
	}]

	final_survey = [{
		'text': 'Which UI provided better recommendations of papers?'
	}, {
		'text': 'Which UI was the most fun to use?'
	}, {
		'text': 'Which UI was the most useful?'
	}, {
		'text': 'Which UI was the easiest to use?'
	}, {
		'text': 'Which UI was the most intuitive?'
	}]

	QuestionItem.objects.all().delete()
	print '=== Post-task Questions'
	for idx, q in enumerate(questions):
		qitem = QuestionItem(
			num = idx+1,
			text = q['text'],
			max_label = q['max_label'],
			min_label = q['min_label'],
			type = 'post-task'
		)
		qitem.save()
		print 'Saved question #' + str(qitem.num) + ' --> ' + qitem.text

	print '\n === Post-study Questions'
	for idx, q in enumerate(final_survey):
		qitem = QuestionItem(
			num = idx+1,
			text = q['text'],
			type = 'post-study'
		)
		qitem.save()
		print 'Saved question #' + str(qitem.num) + ' --> ' + qitem.text



