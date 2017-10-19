from conf_navigator_eval.models import *


def run():
	LatinSquares.objects.all().delete()
	sequences = [
		'CB,SF,CB_SF,HYB',
		'HYB,CB,SF,CB_SF',
		'CB_SF,HYB,CB,SF',
		'SF,CB_SF,HYB,CB'
	]

	for idx, seq in enumerate(sequences):
		LatinSquares.objects.create(
			id = idx+1,
			sequence = seq
		)
		print 'Saved sequence = ' + seq