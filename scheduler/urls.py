from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from scheduler import views

urlpatterns = [
	url(r'^scheduler/$', views.TLEList.as_view()),
	#url(r'^scheduler/(?P<name>[a+z]+)/$', views
]