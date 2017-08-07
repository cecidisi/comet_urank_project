from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'actions', views.LoggedActionViewSet)
router.register(r'post-task-questionnaire', views.PostTaskQuestionnaire)
router.register(r'final-surveys', views.FinalSurveyQuestionnaire)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<task>\d+)/$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^introduction/$', views.introduction, name='introduction'),
    url(r'^set-task/$', views.set_task, name='set-task'), 
    url(r'^set-task/(?P<task>\d+)/$', views.set_task, name='set-task'), 
    url(r'^submit-task/$', views.submit_task, name='submit-task'),   
    url(r'^questions/(?P<task>\d+)/$', views.questions, name='questions'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^submit-questions/$', views.submit_questions, name='submit-questions'),
    url(r'^final-survey/$', views.final_survey, name='final-survey'),
    url(r'^submit-final-survey/$', views.submit_final_survey, name='submit-final-survey'),
    url(r'^finish-task/$', views.finish_task, name='finish-task'),
    url(r'^get-talks/$', views.get_talks, name='get-talks'),
    url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    url(r'^get-neighbors/$', views.get_neighbors, name='get-neighbors'),
    url(r'^urank_service/$', views.urank_service, name='urank_service'),
    url(r'^bookmark-cn/(?P<content_id>\d+)/$', views.bookmark_cn, name='bookmark-cn'),
    url(r'^unbookmark-cn/(?P<content_id>\d+)/$', views.unbookmark_cn, name='unbookmark-cn'),
    url(r'^download-logged-actions/$', views.download_logged_actions, name='download-logged-actions'),
    url(r'^download-post-task-questionnaires/$', views.download_post_task_questionnaires, name='download-post-task-questionnaires'),
    url(r'^download-final-surveys/$', views.download_final_surveys, name='download-final-surveys'),
    url(r'^download-tasks-info/$', views.download_tasks_info, name='download-tasks-info'),
    url(r'^download-bookmarks-eval/$', views.download_bookmarks_eval, name='download-bookmarks-eval'),
    url(r'^', include(router.urls)),
]