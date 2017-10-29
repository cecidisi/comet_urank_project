from rest_framework import serializers
from .models import *


class UpmcUserSerializer(serializers.ModelSerializer):

	class Meta:
		model = UpmcUser
		fields = '__all__'


class UpmcActionLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = UpmcActionLog
		fields = '__all__'


class UpmcTimeLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = UpmcTimeLog
		fields = '__all__'


class UpmcBookmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = UpmcBookmark
		fields = '__all__'

