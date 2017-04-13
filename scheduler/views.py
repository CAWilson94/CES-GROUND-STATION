#from django.shortcuts import get_list_or_404, get_object_or_404
#from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import Http404
from rest_framework.response import Response
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework import status, viewsets  # , generics
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.renderers import StaticHTMLRenderer

from datetime import datetime
from csv_parse import export_csv

from scheduler.models import TLE, Mission, NextPass
from scheduler.services import Services
from scheduler.schedulerServices import SchedulerServices
from scheduler.serializers import TLESerializer, AZELSerializer, MissionSerializer, NextPassSerializer

from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.stochasticHC import MOTStochasticHC
from scheduler.MOT.randomRestartHC import MOTRandomRestartHC
from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.MOT.GAScheduler import MOTGA


from scheduler.tweet import ground_station
from scheduler.tasks import RotatorsThread, SchedulerTask


print("HELLO FROM VIEWS!")
#print("Starting repeating task")
RotatorsThread.delay((NextPass()))

class TLEViewSet(viewsets.ModelViewSet):

    try:
        if(len(TLE.objects.all()) < 1):
            print("Updating TLE data...")
            Services.updateTLE()
            print("...TLE data updated")
    except OperationalError:
        print("Views.TLEViewSet - could not update TLE")
    queryset = TLE.objects.all().order_by("name")
    serializer_class = TLESerializer

class MissionsViewSet(viewsets.ModelViewSet):
    try:
        if(len(Mission.objects.filter(status="NEW")) > 0
            or len(NextPass.objects.filter(setTime__gte=datetime.now())) < 20):
            SchedulerTask.delay()
        queryset = Mission.objects.all()
        serializer_class = MissionSerializer
    except OperationalError:
        queryset = []
        serializer_class = MissionSerializer
        print("MissionsViewSet couldn't be loaded yet")

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

class MissionView(APIView):

    def get(self, request):
        try:
            print("New missions: " + str(len(Mission.objects.filter(status="NEW"))))
            if(len(Mission.objects.filter(status="NEW")) > 0
                or len(NextPass.objects.filter(setTime__gte=datetime.now())) < 20):
                SchedulerTask.delay()

            missions = Mission.objects.all()
            serializer = MissionSerializer(missions, many=True)
            return Response(serializer.data)
        except OperationalError as e:
            print("Couldn't retrieve missions: " + str(e))
            return Response({'Database Error': "Couldn't retrieve missions"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if Services.makeMissions(request.data):
            SchedulerTask.delay()
            return Response({'Creation Successful': request.data.get("name")} ,status=status.HTTP_201_CREATED)
        SchedulerTask.delay()
        return Response({'Database Error': "Couldn't save mission"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        print("deleting: " + str(pk))
        missionToDelete = Mission.objects.filter(id=pk)
        deleted = missionToDelete.delete()
        print("Deleted: " + str(deleted))
        SchedulerTask.delay()
        return Response({'Deleted Successful':deleted},status=status.HTTP_200_OK)


class SchedulerView(APIView):

	def get(self, request):
		isScheduling = False
		if(len(Mission.objects.filter(status="SCHEDULING")) > 0):
			isScheduling = True
		return HttpResponse(isScheduling)

class NextPassView(APIView):

    def get(self, request):
        try:
            passes = NextPass.objects.filter(setTime__gte=datetime.now()).order_by("riseTime")
            serializer = NextPassSerializer(passes, many=True)
            return Response(serializer.data)
        except OperationalError as e: 
            print("Couldn't get next passes: " + str(e))
            return Response({'Database Error': "Couldn't retrieve next passes"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CSVParseView(APIView):
    """view for exporting as csv"""

    def get(self, request):
        return export_csv(request)



"""Testing Views"""

class TestingScheduler():

    def makeMissions(request):
        from random import randint

        print("Updating TLE data...")
        Services.updateTLE()
        print("...TLE data updated")

        picked = []
        tles = TLE.objects.all()
        sats = ""
        for i in range(10):
            tle = tles[randint(0, len(tles) - 1)]
            while tle in picked:
                tle = tles[randint(0, len(tles) - 1)]
            picked.append(tle)
            name = tle.name
            priority = randint(0, 2)
            Mission(name=name, TLE=tle, status="NEW", priority=priority).save()
            sats += tle.name + ", "
            print("Made mission with sat: " + tle.name)
        return HttpResponse("Missions Added: " + sats)

    def schedule(request):
        services = SchedulerServices()
        services.scheduleAndSavePasses()

        string = ""
        for p in NextPass.objects.all():
            string += (p.tle.name + "(" + str(p.mission.priority) + "): "
                       + str(p.riseTime.strftime('%H:%M:%S')) + " -> " + str(p.setTime.strftime('%H:%M:%S')) + "\n\n")
        string = ""
        for p in NextPass.objects.all():
            string += (p.tle.name + "(" + str(p.mission.priority) + "): "
                       + str(p.riseTime.strftime('%H:%M:%S')) + " -> " + str(p.setTime.strftime('%H:%M:%S')) + "\n\n")

        return HttpResponse(string)
        return HttpResponse(string)



# class PyephemData(APIView):

#   def get_object(self, pk):
#       try:
#           return TLE.objects.get(pk=pk)
#       except Snippet.DoesNotExist:
#           raise Http404

#   def get(self, request, pk, format=None):
#       tle = self.get_object(pk)
#       azel = Services.getAzElTLENow(self, tle)  # pass in object?
#       serializer = AZELSerializer(azel)
#       return Response(serializer.data)

class SchedulerCompare():
    """ Schedule comparison output for a select number
    of missions without having to use the GUI"""

    def missionSelect(numMissions):
        """ Pick out the first n satelites from the
                TLE data and generate n missions """
        tles = TLE.objects.all()
        for tle in range(numMissions):
            name = tles[tle].name
            priority = 2
            print("NAME IS " + str(name))
            Mission(name=name, TLE=tles[tle],
                    status="NEW", priority=priority).save()

    def clearMissions():
        Mission.objects.all().delete()

    def schedule():
        SchedulerServices.scheduleAndSavePasses()

    def base_test(missions):
        SchedulerCompare.clearMissions()
        SchedulerCompare.missionSelect(missions)
        SchedulerCompare.schedule()

    def test(request):
        missions = 50

        for i in range(1, missions):
            print("I IS --------------> " + str(i))
            SchedulerCompare.base_test(i)
        SchedulerCompare.clearMissions()
        return HttpResponse("Hurra you did it! ")
