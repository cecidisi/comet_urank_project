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
from .cn_connector import *


urank = Urank()
session_key = 'confnav'


@api_view(['GET', 'POST'])
@csrf_exempt 
def login(request):
    if request.method == 'GET':
        events = DBconnector.get_events()
        template = loader.get_template('conf_navigator/login.html')
        return HttpResponse(template.render({ 'events': events }, request))
    elif request.method == 'POST':
        eventID = request.POST['eventID']
        email = request.POST['email']
        password = request.POST['password']
        # Login with conference navigator, if OK  set session and go to urank
        user = CN_connector.login(email, password)
        if user:
            request.session['user'] = user
            request.session['eventID'] = eventID
            return redirect('/cn_urank')
        else:
            return redirect('/cn_urank/login')



@api_view(['GET', 'POST'])
@csrf_exempt 
def logout(request):
    del request.session['eventID']
    del request.session['user']
    return redirect('login')


@api_view(['GET'])
def index(request):
    if 'user' in request.session and 'eventID' in request.session:
        template = loader.get_template('conf_navigator/index.html')
        return HttpResponse(template.render({}, request))
    return redirect('/cn_urank/login')



@api_view(['GET'])
def test(request):
    print bcolors.OKBLUE + 'Testing with UMAP and Peter' + bcolors.ENDC
    request.session['eventID'] = '149'
    request.session['user'] =  {
        'UserID': '16',
        'name': 'Peter Brusilovsky'
    }
    return redirect('/cn_urank')




'''
    **************      API     *****************
'''

@api_view(['GET'])
def get_talks(request):
    eventID = request.session['eventID']
    print 'get_talks: eventID = ' + str(eventID)
    talks = urank.load_documents(DBconnector.get_documents(eventID))
    resp = {
        'count': len(talks),
        'results': talks
    }
    return Response(resp)


# Get global keywords
@api_view(['GET'])
def get_keywords(request):
    eventID = request.session['eventID']
    print 'get_keywords: eventID = ' + str(eventID)
    keywords = urank.load_keywords(DBconnector.get_keywords(eventID))
    resp = {
        'count': len(keywords),
        'results': keywords
    }
    return Response(resp)



@api_view(['GET'])
def get_neighbors(request):
    user = request.session['user']
    userID = user['UserID']
    eventID = request.session['eventID']
    neighbors = DBconnector.get_neighbors(eventID, userID)
    user_ids = [n['neighbor']['id'] for n in neighbors]
    sim_user_talk = DBconnector.get_sim_user_talk(user_ids)
    neighbors_to_send = urank.load_neighbors(neighbors, sim_user_talk)
    resp = {
        'count': len(neighbors_to_send),
        'results': neighbors_to_send
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



# Get document keywords in string format
@api_view(['GET'])
def get_document_keywords_str(request):
    keywords_str = TalkKeywordStr.objects.all()
    serializer = TalkKeywordStrSerializer(keywords_str, many=True)
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




class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer

