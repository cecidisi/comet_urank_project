from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get-articles/$', views.get_articles, name='get-articles'),
    url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    url(r'^urank_service/$', views.urank_service, name='urank_service'),
    url(r'^', include(router.urls)),
]