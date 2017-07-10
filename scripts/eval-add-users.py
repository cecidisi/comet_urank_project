import sys
import os
import csv
from conf_navigator.models import *
from conf_navigator_eval.models import *


def run():
	email_mapping = get_email_mapping()
	UserEval.objects.all().delete()
	users = User.objects.all()
	for u in users:
		user = UserEval.objects.create(
			id = u.id,
			name = u.name,
			username = u.username,
			email = email_mapping[u.id] if u.id in email_mapping else '',
			type = u.type
		)
		print 'Copied user #' + str(user.pk) + ' ' + user.name + ' to Eval DB (' + user.email + ')'


def get_email_mapping():
	email_mapping = {}
	file_path = '/conf_navigator_eval/files/UMAP-participants.csv'
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file = os.path.join(root_dir + file_path)
	with open(file, 'r') as cvsfile:
		reader = csv.reader(cvsfile, delimiter=',')
		for row in reader:
			user_id = int(row[1])
			email = row[3]
			email_mapping[user_id] = email
			print str(user_id) + ' --> ' + email
		return email_mapping