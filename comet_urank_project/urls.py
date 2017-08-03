"""comet_urank_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.debug import default_urlconf
from django.conf.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 
from django.contrib.staticfiles.views import serve 

urlpatterns = [
    url(r'^urank/comet_urank/', include('comet_urank.urls')),
    url(r'^urank/cn_urank/', include('conf_navigator.urls')),
    url(r'^urank/cn_urank_eval/', include('conf_navigator_eval.urls')),
    url(r'^urank/upmc_urank/', include('upmc_urank.urls')),
    url(r'^urank/admin/', admin.site.urls),    
    # url(r'^$', default_urlconf),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^static/(?P<assets>.*)$', serve), ]
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
else:
    
    urlpatterns += staticfiles_urlpatterns()
