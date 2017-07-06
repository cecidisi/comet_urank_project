# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import * # APIException

from .models import *
from .serializers import *
from .classes.urank_handler import *
from .classes.db_connector import *

urank = Urank()


@api_view(['GET'])
def hello(request):
    return HttpResponse('Hello World!')


@api_view(['GET'])
def index(request):
    template = loader.get_template('comet_urank/index.html')
    return HttpResponse(template.render({}, request))


# Get documents, i.e. colvideos
@api_view(['GET'])
def get_colvideos(request):
    colvideos = urank.load_documents(DBconnector.get_documents())
    resp = {
        'count': len(colvideos),
        'results': colvideos
    }
    return Response(resp)


# Get global keywords
@api_view(['GET'])
def get_keywords(request):
    keywords = urank.load_keywords(DBconnector.get_keywords())
    resp = {
        'count': len(keywords),
        'results' : keywords
    }
    return Response(resp)


# Get usertags from userprofile
@api_view(['GET'])
def get_usertags(request, user_id):
    usertags = DBconnector.get_usertags(user_id)
    usertags = urank.load_usertags(usertags)
    resp = {
        'count' : len(usertags),
        'results' : usertags
    }
    return Response(resp)


@api_view(['GET'])
def get_keyphrases(request, keyword_id):
    keyphrases = DBconnector.get_keyphrases(keyword_id)
    resp = {
        'count': len(keyphrases),
        'results': keyphrases 
    }
    return Response(resp)



# unused
@api_view(['GET'])
def update_ranking(request, query):
    ranked_data = urank.update_ranking(query)
    return Response({
        'count' : len(ranked_data),
        'results': ranked_data
    })



# Get document keywords in string format
@api_view(['GET'])
def get_document_keywords_str(request):
    keywords_str = ColKeywordStr.objects.all()
    serializer = ColKeywordStrSerializer(keywords_str, many=True)
    resp = {
        'results': serializer.data
    }
    return Response(resp)


# @require_http_methods(["POST"])
@api_view(['POST'])
@csrf_exempt 
def urank_service(request): 
    params = json.loads(request.body.decode("utf-8"))
    data_to_send = urank.process_operation(params)
    resp = {
        'count': len(data_to_send),
        'results': data_to_send,
    }
    return Response(resp)







class ColvideoViewSet(viewsets.ModelViewSet):
    queryset = Colvideo.objects.all().order_by('date')
    serializer_class = ColvideoSerializer


# class UsertagViewSet(viewsets.ModelViewSet):
#     queryset = Usertag.objects.filter(fuser_id=user_id).order_by('-count')
#     serializer_class = UsertagSerializer


""" Tagging chunks  """

@api_view(['GET'])
def text_tagging(request):
    data = ColDetailChunk.objects \
        .filter(is_col_desc_man__isnull=True) \
        .exclude(fcol_id__video_url='') \
        .filter(fcol_id__video_url__isnull=False)[:100]
    context = {
        'data' : data
    }
    template = loader.get_template('comet_urank/text_tagging.html')
    return HttpResponse(template.render(context, request))



@api_view(['POST'])
def update_col_desc_man(request):
    print('EN POST')
    data = json.loads(request.POST['data'])
    for d in data:
        cdc_obj = ColDetailChunk.objects.get(pk=d['cdc_id'])
        cdc_obj.is_col_desc_man = d['is_col_desc']
        cdc_obj.save()
        print('SAVED cdc_id = ' + str(cdc_obj.cdc_id) + ' --> ' + str(cdc_obj.is_col_desc_man))
    return HttpResponse(status=200)

