from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^submit-task/$', views.submit_task, name='submit-task'),
    url(r'^bookmark/$', views.bookmark, name='bookmark'),
    url(r'^unbookmark/$', views.unbookmark, name='unbookmark'),
    url(r'^review/$', views.review, name='review'),
    url(r'^review/(?P<user_id>\d+)/$', views.review, name='review'),
    url(r'^download-bookmarks/$', views.download_bookmarks, name='download-bookmarks'),
    url(r'^download-bookmarks/(?P<user_id>\d+)/$', views.download_bookmarks, name='download-bookmarks'),
    url(r'^questionnaire/$', views.questionnaire, name='questionnaire'),

    # url(r'^get-keywords/$', views.get_keywords, name='get-keywords'),
    # url(r'^get-keyphrases/(?P<kw_id>\d+)/$', views.get_keyphrases, name='get-keyphrases'),
    # url(r'^get-facets/(?P<facet_type>\w+)/$', views.get_facets, name='get-facets'),
    # url(r'^get-article-details/(?P<doc_id>\d+)/(?P<decoration>\w+)/$', views.get_article_details, name='get-article-details'),
    # url(r'^search-features/(?P<feature_type>\w+)/(?P<text>\w+)/$', views.search_features, name='search-features'),
    url(r'^update-ranking/$', views.update_ranking, name='update_ranking'),
    # url(r'^urank-service/$', views.urank_service, name='urank_service'),
    url(r'^filter-articles-by-year/(?P<from_year>\d+)/(?P<to_year>\d+)/$', views.filter_articles_by_year, name='filter-articles-by-year'),
    url(r'^get-more-articles/(?P<current_count>\d+)/$', views.get_more_articles, name='get-more-articles'),
    url(r'^get-more-articles/(?P<user_id>\d+)/(?P<current_count>\d+)/$', views.get_more_articles, name='get-more-articles'),
]