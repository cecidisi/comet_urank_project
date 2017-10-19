from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from conf_navigator.models import *
from conf_navigator.serializers import *
import json

class DBconnector:

	@classmethod
	def get_events(cls):
		events = Event.objects.all()
		return EventSerializer(events, many=True).data


	@classmethod
	def get_documents(cls, eventID):
		# event = Event.objects.get(pk=eventID)
		talks = Talk.objects.filter(event_id=eventID)
		talks = TalkSerializer.setup_eager_loading(talks)
		return TalkSerializer(talks, many=True).data
	

	@classmethod
	def get_keywords(cls, eventID):
		# event = Event.objects.get(pk=eventID)
		keywords = ConfGlobalKeyword.objects.filter(event_id=eventID)
		return ConfGlobalKeywordSerializer(keywords, many=True).data
		# Return after renaming colvideos as appears_in
		# keywords = [ dict(k, **{'appears_in' : k.pop('colvideos')}) for k in keywords]
		# return keywords


	@classmethod
	def get_keyphrases(cls, keyword_id):
		keyword = ConfGlobalKeyword.objects.get(pk=keyword_id)
		print keyword
		try:
			keyphrases =TalkKeyphraseSerilizer(keyword.keyphrases.all(), many=True).data
			for kp in keyphrases:
				kp['sequence'] = json.loads(kp['sequence'])
			return keyphrases
		except Keyphrase.DoesNotExist:
			return []


	@classmethod
	def get_neighbors(cls, eventID, userID):
		neighbors = SimUserNeighbor.objects.filter(event_id=eventID).filter(user_id=userID).order_by('-score')
		neighbors = SimUserNeighborSerializer(neighbors, many=True).data
		for v in neighbors:
			v['explanations'] = json.loads(v['explanations'])
		return neighbors


	@classmethod
	def get_sim_user_talk(cls, user_ids):
		sim_user_talk = SimUserTalk.objects.filter(user_id__in=user_ids)
		return SimUserTalkSerializer(sim_user_talk, many=True).data



