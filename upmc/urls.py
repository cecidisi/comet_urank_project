from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get-articles/$', views.get_articles, name='get-articles'),
    url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    url(r'^get-keyphrases/(?P<kw_id>\d+)/$', views.get_keyphrases, name='get-keyphrases'),
    url(r'^get-article-details/(?P<doc_id>\d+)/(?P<decoration>\w+)/$', views.get_article_details, name='get-article-details'),
    url(r'^search-features/(?P<feature_type>\w+)/(?P<text>\w+)/$', views.search_features, name='search-features'),
    url(r'^update-ranking/$', views.update_ranking, name='update_ranking'),
    url(r'^urank_service/$', views.urank_service, name='urank_service'),
    url(r'^', include(router.urls)),
]