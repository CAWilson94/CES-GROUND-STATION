from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from scheduler import views

urlpatterns = [
	url(r'^scheduler/$', views.TLEList.as_view()),
	url(r'^scheduler/(?P<pk>[0-9]+)/$', views.TLEDetail.as_view()),
	url(r'^', views.TLEList.as_view()),
]#this order matters

urlpatterns = format_suffix_patterns(urlpatterns)