from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from scheduler import views
from scheduler.views import TLEViewSet, PyephemData
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(prefix='tles', viewset=TLEViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # 	#url(r'^updateTLE/$',views.TLEUpdate.as_view()),
    # 	url(r'^$', TLEList.as_view()),
    # 	url(r'^scheduler/?$', views.TLEList.as_view()),
    # 	url(r'^scheduler/(?P<pk>[0-9]+)/?$', views.TLEDetail.as_view()),
    url(r'^tles/(?P<pk>[0-9]+)/azel/?$', views.PyephemData.as_view()),
    url(r'^postdata/(?P<nameArray>[a-z]+)/?$', views.postEx.as_view()),
    url(r'^postdata/?$', views.postEx.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
