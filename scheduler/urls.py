from django.conf.urls import url
from . import views

app_name = 'scheduler'
urlpatterns = [
	#ex: /scheduler/	
    url(r'^$', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^updateTLE1', views.updateTLE1, name='updateTLE1'),
]