
from django.core.exceptions import ObjectDoesNotExist

from upmc_study.models import *
from upmc_study.serializers import *


class DBconnector:

	@classmethod
	def get_user(cls, username):
		try:
			user = UpmcUser.objects.get(username=username)
			return UpmcUserSerializer(user).data
		except ObjectDoesNotExist:
			return False


	@classmethod
	def get_bookmarks(cls, user_id):
		bookmarks = UpmcBookmark.objects.filter(upmc_user_id=user_id)
		return UpmcBookmarkSerializer(bookmarks, many=True).data




