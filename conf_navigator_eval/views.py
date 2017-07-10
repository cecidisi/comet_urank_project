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

from conf_navigator.models import *
from conf_navigator.serializers import *
from conf_navigator.classes.urank_handler import *
from conf_navigator.classes.db_connector import *
from conf_navigator.classes.authentication import *
from conf_navigator.classes.bcolors import *

from .classes.task_manager import *



urank = Urank()
tm = TaskManager()



@api_view(['GET', 'POST'])
@csrf_exempt 
def login(request):
    # GET login
    if request.method == 'GET':
        events = DBconnector.get_events()
        template = loader.get_template('conf_navigator_eval/login.html')
        return HttpResponse(template.render({ 'events': events }, request))
    # POST login
    elif request.method == 'POST':
        eventID = request.POST['eventID']
        email = request.POST['email']
        password = request.POST['password']
        # Login with conference navigator, if OK  set session and go to urank
        user = Auth.login(email, password)
        if user:
            request.session.flush()
            request.session['eventID'] = eventID
            request.session['user'] = user
            tm.set_user(user['UserID'])
            return redirect('/cn_urank_eval/set-task')
        else:
            return redirect('/cn_urank_eval/login')



@api_view(['GET', 'POST'])
@csrf_exempt 
def logout(request):
    request.session.flush()
    return redirect('test')
    # return redirect('login')



@api_view(['GET'])
def test(request):
    print_blue('Testing with UMAP and Peter')
    request.session.flush()
    request.session['eventID'] = '149'
    user = {
        'UserID': '16',
        'name': 'Peter Brusilovsky'
    }
    request.session['user'] = user
    return redirect('/cn_urank_eval/set-task')



@api_view(['GET'])
def index(request, task=1):
    if 'user' in request.session and 'eventID' in request.session and 'settings' in request.session:
        settings = request.session['settings']
        print_blue('Settings -> rs = ' + settings['rs'] + \
            ', use_tagcloud = ' + str(settings['use_tagcloud']) + \
            ', use_neighborcloud = ' + str(settings['use_neighborcloud']))
        template = loader.get_template('conf_navigator_eval/index.html')
        return HttpResponse(template.render(settings, request))
    return redirect('/cn_urank_eval/login')

'''
    **************      EVALUATION     *****************
'''

@api_view(['GET', 'POST'])
def questions(request, task=1):
    if request.method == 'GET':
        template = loader.get_template('conf_navigator_eval/questions.html')
        questions = tm.get_questions()
        context = {
            'task': request.session['cur_task'],
            'questions': questions,
            'likert': [1,2,3,4,5,6,7]
        }
        return HttpResponse(template.render(context, request))
    else:
        print request.POST['question-1']
        # params = json.loads(request.body.decode("utf-8"))
    
        return Response({})




@api_view(['POST'])
@csrf_exempt 
def submit_questions(request):
    values = json.loads(request.body)['values']
    if tm.save_questions(values):
        return Response({ 'results': 'OK' })
    return Response({}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def set_task(request):
    tot_tasks = 4
    if 'cur_task' not in request.session:
        # Init task
        request.session['cur_task'] = 1
        request.session['task_list'] = tm.get_eval_setting_list()
        tm.clear()
        tm.set_user(request.session['user']['UserID'])
    elif request.session['cur_task'] < tot_tasks:
        # Update task
        request.session['cur_task'] = request.session['cur_task'] + 1
        tm.next_task()
    else:
        # Finish task
        return redirect('/cn_urank_eval/finish-task/')

    cur_task = request.session['cur_task']
    task_list = request.session['task_list']
    print_blue('Task List = ' + str(', '.join(task_list)))
    print_blue('Current Task = ' +str(cur_task))
    idx = cur_task - 1
    rs = str(task_list[idx])
    request.session['settings'] =  {
        'rs': rs,
        'use_tagcloud': True if rs != 'SF' else False,
        'use_neighborcloud': True if rs != 'CB' else False
    }
    request.session.modified = True
    return redirect('/cn_urank_eval/'+str(cur_task)+'/')


# Finish View
@api_view(['GET'])
def finish_task(request):
    request.session.flush()
    template = loader.get_template('conf_navigator_eval/finish.html')
    print_blue('Finished Task')
    return HttpResponse(template.render({}, request))




@api_view(['POST'])
@csrf_exempt 
def submit_task(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode("utf-8"))
        if tm.save_task(params):
            return Response({ 'results': 'OK' })
        return Response({}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return redirect('/cn_urank_eval/set-task');
        





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

