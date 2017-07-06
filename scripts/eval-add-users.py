from conf_navigator.models import *
from conf_navigator_eval.models import *


def run():
	users = User.objects.all()
	for user in users:
		ueval = UserEval.objects.create(
			id = user.id,
			name = user.name,
			username = user.username,
			type = user.type
		)
		print 'copied user #' + str(ueval.pk) + ' ' + ueval.name + ' to Eval DB'