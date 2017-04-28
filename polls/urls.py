from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.upload_content, name='main-page'),
    url(r'^thanks/$',views.thanks, name='thanks'),
    #url(r'^download/$',views.download, name='download'),
]