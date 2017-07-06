from rest_framework import serializers
from conf_navigator_eval.models import *


class LatinSquaresSerializer(serializers.ModelSerializer):
	class Meta:
		model = LatinSquares
		fields = '__all__'


class EvalSettingSerializer(serializers.ModelSerializer):
	ltsq = LatinSquaresSerializer(read_only=True)
	def setup_eager_loading(cls, queryset):
		queryset = queryset.prefetch_related('ltsq')
		return queryset

	class Meta:
		model = EvalSetting
		fields = ('id', 'date', 'ltsq')
