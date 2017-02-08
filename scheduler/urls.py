from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from scheduler import views
#from scheduler.views import TLEList, TLEDetail, 
from scheduler.views import TLEViewSet
from rest_framework.routers import DefaultRouter



# urlpatterns = [
# 	#url(r'^updateTLE/$',views.TLEUpdate.as_view()),
# 	url(r'^$', TLEList.as_view()),
# 	url(r'^scheduler/?$', views.TLEList.as_view()),
# 	url(r'^scheduler/(?P<pk>[0-9]+)/?$', views.TLEDetail.as_view()),
# 	url(r'^scheduler/(?P<pk>[0-9]+)/azel/?$',views.PyephemData.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

router = DefaultRouter()
router.register(prefix='tles', viewset=TLEViewSet)
urlpatterns = router.urls