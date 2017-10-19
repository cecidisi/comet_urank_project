'''
Read participant list, populate Users
Link user <-> event
'''

import sys
import os
import csv
import urllib2
from bs4 import BeautifulSoup as bs
from django.core.exceptions import ObjectDoesNotExist
from conf_navigator.models import *
from helper.bcolors import *


def run():
	url_temp = 'http://halley.exp.sis.pitt.edu/cn3mobile/userlist.jsp?eventID=[eventID]'
	filepath_temp = '/conf_navigator/files/attendee_[eventID].xml'
	# files = ['attendee_149.xml', 'attendee_150.xml']
	conf_ids = [149, 150]

	delete_from_db()
	for cid in conf_ids:
		# fetch event
		event = Event.objects.get(pk=cid)
		# Try to read from url
		url = url_temp.replace('[eventID]', str(cid))
		print '\nRead url --> ' + url
		data = read_url(url)
		# If url fails, read file
		if data is None:
			filepath = filepath_temp.replace('[eventID]', str(cid))
			print 'URL failed, read from file --> ' + filepath + '\n'
			data = read_file(filepath)

		participant_csv = get_participants_from_list() if cid == 149 else []
		process_participants(data, participant_csv, event)



def read_url(url):
	resp =  urllib2.urlopen(url).read()
	soup = bs(resp, 'xml')
	try:
		data = soup.find_all('Item')
		if len(data):
			return data
		return None
	except Exception, e:
		print_red(str(e))
		return None


def read_file(file_path):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(root_dir + file_path)
	handler = open(file_path).read()
	soup = bs(handler, 'xml')
	return soup.find_all('Item')


def delete_from_db():
	User.objects.all().delete()


def process_participants(participants, participant_csv, event):
	participant_dict = {}

	for p in participants:
		user, created = User.objects.get_or_create(
			id = p.find('userID').get_text(),
			name = p.find('name').get_text(),
			username = p.find('username').get_text()
		)
		if created:
			participant_dict[user.id] = True
			print 'Saved user #' + str(user.pk) + ' --> name = '+ user.name
		user.events.add(event)

	print '---------------------------------'
	for p in participant_csv:
		if p['id'] not in participant_dict:
			user, created = User.objects.get_or_create(
				id = p['id'],
				name = p['name'],
				username = p['name'].replace(' ', '_')
			)
			if created:
				participant_dict[user.id] = True
				print 'Saved user from CSV #' + str(user.pk) + ' --> name = '+ user.name
			user.events.add(event)



def get_participants_from_list():
	participant_csv = []
	file_path = '/conf_navigator_eval/files/UMAP-participants.csv'
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file = os.path.join(root_dir + file_path)
	with open(file, 'r') as cvsfile:
		reader = csv.reader(cvsfile, delimiter=',')
		for row in reader:
			user_id = row[1]
			name = row[2]
			participant_csv.append({ 'id': user_id, 'name': name })
			print str(user_id) + ' --> ' + name
		return participant_csv

