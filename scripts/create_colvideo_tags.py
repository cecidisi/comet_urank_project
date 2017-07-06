import json
from comet_urank.models import *



def create_colvideo_tags():
	ColvideoTagStr.objects.all().delete()

	colvideos = Colvideo.objects.all()
	n = len(colvideos)
	for i, cv in enumerate(colvideos):
		usertags = Usertag.objects.filter(colvideos__pk=cv.pk)
		if len(usertags):
			tags = ' '.join([u.tag for u in usertags])
			cts = ColvideoTagStr(tag_str=tags, colvideo=cv)
			cts.save()
			print '('+str(i+1)+'/'+str(n)+') Saved tag string' + tags



def run():
	create_colvideo_tags()