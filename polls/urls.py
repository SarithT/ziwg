from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^new/$', views.upload_content, name='new'),
    url(r'^$',views.index, name='index'),
    url(r'^all/$',views.all, name='all'),
    #url(r'^download/$',views.download, name='download'),
]