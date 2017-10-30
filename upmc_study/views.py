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
import ujson
import csv
from itertools import chain

from helper.bcolors import *
from urank_service.urank_handler import *
from upmc.search import eSearch
from .db_connector import *
from .task_manager import *

num_documents = 30
num_keywords = 100
urank = Urank(num_documents=num_documents)


@api_view(['GET'])
def index(request):
    if 'user_id' not in  request.session:
        return redirect('/urank/upmc-study/login')

    template = loader.get_template('upmc_study/index.html')
    return HttpResponse(template.render({ 
    	'user_id': request.session['user_id']
    }, request))



@api_view(['GET', 'POST'])
@csrf_exempt 
def login(request):
    # GET login
    if request.method == 'GET':
        template = loader.get_template('upmc_study/login.html')
        return HttpResponse(template.render({}, request))
    # POST login
    elif request.method == 'POST':
        username = request.POST['username']
        user = DBconnector.get_user(username)
        if user:
            print 'Session set for ' + username + '(id='+str(user['id'])+')'
            request.session.flush()
            request.session['username'] = username
            request.session['user_id'] = user['id']
            return redirect('/urank/upmc-study/')
        else:
            return redirect('/urank/upmc-study/login')



@api_view(['GET', 'POST'])
@csrf_exempt 
def logout(request):
    request.session.flush()
    # return redirect('test')
    return redirect('login')



@api_view(['GET'])
def review(request, user_id=None):
    user_id = user_id or request.session['user_id']
    bookmarks = TaskManager.get_bookmarks(user_id)
    template = loader.get_template('upmc_study/review.html')
    context = {
    	'bookmarks': bookmarks
    }
    return HttpResponse(template.render(context, request))



def write_csv(csv_data, filename):
    keys = csv_data[0].keys()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
    writer = csv.DictWriter(response, keys) 
    writer.writeheader()
    # writer.writerows([unicode(d).encode("utf-8") for d in  csv_data])
    writer.writerows(csv_data)
    return response



@api_view(['GET'])
def download_bookmarks(request, user_id=None):
    user_id = user_id or request.session['user_id']
    bookmarks = TaskManager.get_bookmarks(user_id)
    for b in bookmarks:
        b['title'] = b['title'].encode("utf-8")
        b['abstract'] = b['abstract'].encode("utf-8")
    # print bookmarks[0]
    return write_csv(bookmarks, 'my-bookmarks')



@api_view(['GET'])
def questionnaire(request):
    # logout before filling questionnaire
    request.session.flush()
    template = loader.get_template('upmc_study/questionnaire.html')
    return HttpResponse(template.render({}, request))



# Submit Task (bookmarks and action logs)
@api_view(['POST'])
@csrf_exempt 
def submit_task(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode("utf-8"))
        if TaskManager.save_task(params):
            return Response({ 'message': 'OK' })
        return Response({ 'message': 'Error saving task'})
        # return Response({ 'message': 'Error saving task'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



# Bookmark
@api_view(['POST'])
def bookmark(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode("utf-8"))
        print params
    	TaskManager.bookmark(params)
    	return Response({ 'results': 'OK' })
    


# Unbookmark
@api_view(['POST'])
def unbookmark(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode("utf-8"))
    	TaskManager.unbookmark(params)
    	return Response({ 'results': 'OK' })



@api_view(['GET'])
def get_bookmarks(request, user_id):
    bookmarks = TaskManager.get_bookmarks(user_id)
    resp = {
        'results': bookmarks,
        'count': len(bookmarks)
    }
    return Response(resp)





'''
	URANK
'''


# Update
@api_view(['POST'])
@csrf_exempt 
def update_ranking(request): 
    params = ujson.loads(request.body.decode("utf-8"))
    # Add user on update!!!
    user_id = params['user'] if params['user'] is not None else request.session['user_id']
    query = [q['stem'].split(' ') for q in params['features']['keywords']]
    query = list(chain.from_iterable(query))
    print query
    # articles = eSearch.search_by_keywords(stems=query, { 'keywords': True })
    articles = eSearch.search_by_keywords(stems=query, keywords=True)
    count = len(articles)
    articles = urank.update_ranking(params, articles)
    ids_list = [d['id'] for d in articles]
    # positions = eSearch.get_text_positions(ids_list)
    positions = eSearch.search_by_ids(ids_list, pos_title=True, pos_abstract=True)
    decoration = params['decoration'] or None
    ranked_articles = urank.get_styled_documents(articles, positions, decoration)
    # Mark bookmarked items
    bookmarks = DBconnector.get_bookmarks(user_id)
    ranked_articles = TaskManager.mark_bookmarked(ranked_articles, bookmarks)

    print_blue(str(count))
    resp = {
        'count': count,
        'results': ranked_articles,
    }
    return Response(resp)



# Year Filtering
@api_view(['GET'])
def filter_articles_by_year(request, from_year, to_year):
    filtered_articles = urank.filter_by_year(from_year, to_year)
    if len(filtered_articles) == 0:
        # eSearch.search_by_keywords('migrain', { 'year_range': [from_year, to_year] })
        eSearch.search_by_keywords('migrain', year_range=[from_year, to_year])
    resp = {
        'count': len(filtered_articles),
        'results': filtered_articles
    }
    return Response(resp)



@api_view(['GET'])
def get_more_articles(request, user_id=None, current_count=None):
    user_id = user_id or request.session['user_id']
    more_articles = urank.get_more_results()
    print_blue('current count = ' + str(current_count))

    if len(more_articles):
        ids_list = [d['id'] for d in more_articles]
        positions = eSearch.search_by_ids(ids_list, pos_title=True, pos_abstract=True)
        decoration = 'underline'
        ranked_articles = urank.get_styled_documents(more_articles, positions, decoration)
        # Mark bookmarked items
        bookmarks = DBconnector.get_bookmarks(user_id)
        ranked_articles = TaskManager.mark_bookmarked(ranked_articles, bookmarks)
    else:
        current_count = int(current_count)
        count = current_count + num_documents
        print 'count = ' + str(count)
        more_articles = eSearch.search_by_keywords(['migrain'], offset=current_count, count=count)

    resp = {
        'results': more_articles,
        'count': len(more_articles)
    }
    return Response(resp)        




@api_view(['GET'])
def get_article_details(request, doc_id, decoration):
    article = eSearch.search_by_ids([doc_id], abstract=True, pos_title=True, pos_detail=True)[0]
    resp = { 'count': 0, 'results': None}
    print decoration
    if article:
        resp = { 
            'count': 1, 
            'results': urank.get_document_details(article, decoration) 
        }
    return Response(resp)



