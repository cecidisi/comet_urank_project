from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
import unicodedata
from comet_urank.models import *

def create_col_video():
	Colvideo.objects.all().delete()
	colloquia = Colloquium.objects.exclude(video_url='').filter(video_url__isnull=False)
	n = len(colloquia)
	for i, c in enumerate(colloquia):
		parsed_title = BeautifulSoup(c.title, 'html.parser').get_text()
		title = unicodedata.normalize('NFKD', parsed_title).encode('ascii','ignore')
		parsed_detail = BeautifulSoup(c.detail, 'html.parser').get_text()
		detail = unicodedata.normalize('NFKD', parsed_detail).encode('ascii','ignore')
		user = None
		try:
			user = Userinfo.objects.get(pk=c.user_id)
		except Userinfo.DoesNotExist:
			user = None
		speaker = None
		try:
			speaker = Speaker.objects.get(pk=c.speaker_id)
		except Speaker.DoesNotExist:
			speaker = None

		colvideo = Colvideo(title=title, detail=detail, date=c.field_date, location=c.location,
			url=c.url, video_url=c.video_url, paper_url=c.paper_url, slide_url=c.slide_url,
			colloquium=c, user=user, speaker=speaker, s_bio=c.s_bio)
		colvideo.save()
		print '('+ str(i+1) + '/' + str(n) +') saved colvideo' 




def run():
	create_col_video()