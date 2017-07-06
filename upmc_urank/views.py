# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.conf import settings

from django.shortcuts import render, HttpResponse
from django.template import loader

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv


@api_view(['GET'])
def hello(request):
    return HttpResponse('Hello World!')

@api_view(['GET'])
def index(request):
    template = loader.get_template('upmc_urank/index.html')
    return HttpResponse(template.render({}, request))


@api_view(['GET'])
def get_data(response):
	print(os.path.join(settings.STATIC_URL, 'datasets/pubmed_result.csv'))
	# with open(os.path.join(settings.STATIC_URL, 'datasets/pubmed_result.csv'), 'rb').read()
	# 	# res_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	# 	res_reader = csv.reader(csvfile, delimiter=',')
	# 	for row in res_reader:
	# 		print ', '.join(row)

	resp = {
		'results' :[]
	}
	return Response(resp)