from django.conf.urls import url

from . import views

app_name = 'web'
urlpatterns = [
    url(r'^$', views.upload_file, name='upload'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #url(r'^upload/$', views.upload_file, name='upload'),
]
