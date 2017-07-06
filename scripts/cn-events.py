
from conf_navigator.models import *


def get_date(date):
	return datetime.datetime.strptime(date, "%m-%d-%Y")


def create_sessions():
	event_umap = Event.objects.create(
		id=149, title='UMAP 2017', begin_date=get_date('07-09-2017'), 
		end_date=get_date('07-12-2017'), type='Conference')

	print 'Saved event ' + event_umap.title
		
	event_ht = Event.objects.create(
		id=150, title='Hypertext 2017', begin_date=get_date('07-04-2017'), 
		end_date=get_date('07-07-2017'), type='Conference') 

	print 'Saved event ' + event_ht.title


def run():
	Event.objects.all().delete()
	create_sessions()
	