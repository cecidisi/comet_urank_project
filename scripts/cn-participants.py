'''
Read participant list, populate Users
Link user <-> event
'''


import sys
import os
import urllib2
from bs4 import BeautifulSoup as bs
from django.core.exceptions import ObjectDoesNotExist
from conf_navigator.models import *


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

		process_participants(data, event)



def read_url(url):
	resp =  urllib2.urlopen(url).read()
	soup = bs(resp, 'xml')
	try:
		data = soup.find_all('Item')
		if len(data):
			return data
		return None
	except:
		return None


def read_file(file_path):
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(root_dir + file_path)
	handler = open(file_path).read()
	soup = bs(handler, 'xml')
	return soup.find_all('Item')


def delete_from_db():
	User.objects.all().delete()


def process_participants(participants, event):
	for p in participants:
		user, created = User.objects.get_or_create(
			id = p.find('userID').get_text(),
			name = p.find('name').get_text(),
			username = p.find('username').get_text()
		)
		if created:
			print 'Saved user #' + str(user.pk) + ' --> name = '+ user.name + '; username = ' + user.username
		user.events.add(event)




