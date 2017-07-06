from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from comet_urank.models import *
from comet_urank.serializers import *
import json

class DBconnector:

	@classmethod
	def get_documents(cls):
		colvideos = Colvideo.objects.all().order_by('date')#[:100]
		colvideos = ColvideoSerializer.setup_eager_loading(colvideos)
		return ColvideoSerializer(colvideos, many=True).data


	@classmethod
	def get_keywords(cls):
		keywords = GlobalKeywordSerializer(GlobalKeyword.objects.all(), many=True).data
		# Return after renaming colvideos as appears_in
		# keywords = [ dict(k, **{'appears_in' : k.pop('colvideos')}) for k in keywords]
		return keywords


	@classmethod
	def get_usertags(cls, user_id):
		queryset = Usertag.objects.filter(user_id=user_id).order_by('-count')
		return UsertagSerializer(queryset, many=True).data


	@classmethod
	def get_keyphrases(cls, keyword_id):
		keyword = GlobalKeyword.objects.get(pk=keyword_id)
		print keyword
		try:
			keyphrases =KeyphraseSerilizer(keyword.keyphrases.all(), many=True).data
			for kp in keyphrases:
				kp['sequence'] = json.loads(kp['sequence'])
			return keyphrases
		except Keyphrase.DoesNotExist:
			return []




