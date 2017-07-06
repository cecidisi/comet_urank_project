from django.conf.urls import url, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'talks', views.TalkViewSet)


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<task>\d+)/$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set-task/$', views.set_task, name='set-task'), 
    url(r'^submit-task/$', views.submit_task, name='submit-task'),   
    url(r'^questions/(?P<task>\d+)/$', views.questions, name='questions'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^submit-questions/$', views.submit_questions, name='submit-questions'),
    url(r'^finish-task/$', views.finish_task, name='finish-task'),
    url(r'^get-talks/$', views.get_talks, name='get-talks'),
    url(r'^get-document-keywords-str/$', views.get_document_keywords_str, name='get-document-keywords-str'),
    url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    url(r'^get-neighbors/$', views.get_neighbors, name='get-neighbors'),
    url(r'^get-keyphrases/(?P<keyword_id>\d+)/$', views.get_keyphrases, name='get-keyphrases'),
    url(r'^urank_service/$', views.urank_service, name='urank_service'),
    url(r'^', include(router.urls)),
]