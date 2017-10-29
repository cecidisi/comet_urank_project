import sys
import os
import csv
from upmc_study.models import *


def run():
	UpmcUser.objects.all().delete()

	file_path = '/files/class_list.csv'
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file = os.path.join(root_dir + file_path)

	users = 0
	with open(file, 'r') as cvsfile:
		reader = csv.reader(cvsfile, delimiter=',')
		# skip header
		reader.next()
		for row in reader:
			user = UpmcUser(
				first_name = row[0],
				last_name = row[1],
				username = row[2]
			)
			user.save()
			users += 1
			
		print 'Saved ' + str(users) + ' users'

	# add test user
	user = UpmcUser(
		first_name = 'test',
		last_name = 'test',
		username = 'test'
	)
	user.save()

		





