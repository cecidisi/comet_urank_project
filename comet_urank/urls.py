from django.conf.urls import url, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'colvideos', views.ColvideoViewSet)
# router.register(r'usertag', views.UsertagViewSet)


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^get-colvideos/$', views.get_colvideos, name='get-colvideos'),
    url(r'^get-document-keywords-str/$', views.get_document_keywords_str, name='get-document-keywords-str'),
    url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    url(r'^get-usertags/(?P<user_id>\d+)/$', views.get_usertags, name='get-usertags'),
    url(r'^get-keyphrases/(?P<keyword_id>\d+)/$', views.get_keyphrases, name='get-keyphrases'),
    # url(r'^update-ranking/(?P<query>\d+)/$', views.update_ranking, name='update-ranking'),
    url(r'^urank_service/$', views.urank_service, name='urank_service'),
    url(r'^text_tagging/$', views.text_tagging, name='text_tagging'),
    url(r'^update_col_desc_man/$', views.update_col_desc_man, name='update_col_desc_man'),
    url(r'^', include(router.urls)),
]