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
from itertools import chain
import ujson

from helper.bcolors import *
from urank_service.urank_handler import *
from .db_connector import *
from .search import *

num_documents = 30
num_keywords = 100
urank = Urank(num_documents=num_documents)


@api_view(['GET'])
def index(request):
    template = loader.get_template('upmc/index.html')
    return HttpResponse(template.render({}, request))


'''
    **************      API     *****************
'''

@api_view(['GET'])
def get_articles(request):
    # articles = urank.load_documents(DBconnector.get_articles())
    articles = eSearch.search_by_keywords(['migrain'], count=num_documents)
    resp = {
        'count': len(articles),
        'results': articles
    }
    return Response(resp)



# Get global keywords
@api_view(['GET'])
def get_keywords(request):    
    # keywords = urank.load_keywords(DBconnector.get_keywords())
    keywords = eSearch.get_global_keywords(num_keywords)
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
    print decoration
    if article:
        resp = { 
            'count': 1, 
            'results': urank.get_document_details(article, decoration) 
        }
    return Response(resp)



@api_view(['GET'])
def search_features(request, feature_type, text):
    print_blue('feature_type = ' + feature_type + '; text = '+ text)
    features = DBconnector.search_features(feature_type, text)[:100]
    resp = {
        'count': len(features),
        'results': features
    }
    return Response(resp)




@api_view(['GET'])
def  get_facets(request, facet_type):
    resp = { 'count': 0, 'results': [] }
    if facet_type == 'year':
        year_facets = DBconnector.get_year_facets()
        resp['count'] = len(year_facets)
        resp['results'] = year_facets 
    
    return Response(resp)



@api_view(['GET'])
def filter_articles_by_year(request, from_year, to_year):
    filtered_articles = urank.filter_by_year(from_year, to_year)
    if len(filtered_articles) == 0:
        eSearch.search_by_keywords('migrain', year_range=[from_year, to_year])
    resp = {
        'count': len(filtered_articles),
        'results': filtered_articles
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



@api_view(['POST'])
@csrf_exempt 
def update_ranking(request): 
    params = ujson.loads(request.body.decode("utf-8"))
    query = [q['stem'].split(' ') for q in params['features']['keywords']]
    query = list(chain.from_iterable(query))
    print query
    articles = eSearch.search_by_keywords(stems=query, keywords=True)
    articles = urank.update_ranking(params, articles)
    ids_list = [d['id'] for d in articles]
    positions = eSearch.search_by_ids(ids_list, pos_title=True, pos_abstract=True)
    decoration = params['decoration'] or None
    ranked_articles = urank.get_styled_documents(articles, positions, decoration)

    resp = {
        'count': len(ranked_articles),
        'results': ranked_articles,
    }
    return Response(resp)





class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = PubmedGlobalKeyword.objects.all()
    serializer_class = PubmedGlobalKeywordSerializer

