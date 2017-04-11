from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from scheduler import views
from scheduler.views import TLEViewSet, MissionView, NextPassView, MissionsViewSet, CSVParseView, TestingScheduler, SchedulerView, SchedulerCompare
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(prefix='missions', viewset=MissionsViewSet)
router.register(prefix='tles', viewset=TLEViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # 	#url(r'^updateTLE/$',views.TLEUpdate.as_view()),
    url(r'^save/mission/?$', MissionView.as_view()),
    url(r'^delete/mission/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})?$',
        MissionView.as_view()),
    #url(r'^nextpass/?$', MissionView.as_view()),
    url(r'^missions/(?P<pk>[0-9]+)/?$', MissionView.as_view()),
    #url(r'^missions/?$', MissionView.as_view()),
    url(r'csv/missions/?$', CSVParseView.as_view()),
    url(r'^scheduler/isscheduling/?$', SchedulerView.as_view()),
    url(r'^nextpass/get/?$', NextPassView.as_view()),
    url(r'^mission/get/?$', MissionView.as_view()),

    # Testing urls
    #url(r'^tles/(?P<pk>[0-9]+)/azel/?$', PyephemData.as_view()),
    #url(r'^schedulemissiontest/?$', MissionView.as_view()),
    url(r'^makemissions/?$', TestingScheduler.makeMissions, name="makeMissions"),
    url(r'^schedule/?$', TestingScheduler.schedule, name="schedule"),
    url(r'^thread/?$', TestingScheduler.threadTask, name="thread"),
    url(r'scheduler/comparison/?$', SchedulerCompare.test),

]
