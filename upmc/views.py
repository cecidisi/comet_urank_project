# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import * # APIException
import json

from helper.bcolors import *
from urank_service.urank_handler import *
from .models import *
from .serializers import *
from .db_connector import *

urank = Urank()


@api_view(['GET'])
def index(request):
    template = loader.get_template('upmc/index.html')
    return HttpResponse(template.render({}, request))


'''
    **************      API     *****************
'''

@api_view(['GET'])
def get_articles(request):
    articles = urank.load_documents(DBconnector.get_articles())
    resp = {
        'count': len(articles),
        'results': articles
    }
    return Response(resp)



# Get global keywords
@api_view(['GET'])
def get_keywords(request):    
    keywords = urank.load_keywords(DBconnector.get_keywords())
    resp = {
        'count': len(keywords),
        'results': keywords
    }
    return Response(resp)


@api_view(['GET'])
def get_keyphrases(request, kw_id):
    keyphrases = DBconnector.get_keyphrases(kw_id)
    resp = {
        'count': len(keyphrases),
        'results': keyphrases
    }
    return Response(resp)



@api_view(['GET'])
def get_article_details(request, doc_id, decoration):
    article = DBconnector.get_article_details(doc_id)
    
    resp = { 'count': 0, 'results': None}
    if article:
        resp = { 
            'count': 1, 
            'results': urank.get_document_details(article, decoration) 
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




class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = PubmedGlobalKeyword.objects.all()
    serializer_class = PubmedGlobalKeywordSerializer

