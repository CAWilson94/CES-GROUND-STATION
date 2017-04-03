from django.http import HttpResponse
from django.http import Http404
#from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.utils import OperationalError
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
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
from scheduler.tasks import RotatorsThread


print("HELLO FROM VIEWS!")
#print("Starting repeating task")
RotatorsThread.delay((NextPass()))


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

    def threadTask(request):
        # print("Starting repeating task")
        # repeatingTask.delay()
        return HttpResponse("Started task")

    def schedule(request):
        services = SchedulerServices()
        services.scheduleAndSavePasses()

        string = ""
        for p in NextPass.objects.all():
            string += (p.tle.name + "(" + str(p.mission.priority) + "): "
                       + str(p.riseTime.strftime('%H:%M:%S')) + " -> " + str(p.setTime.strftime('%H:%M:%S')) + "\n\n")

        return HttpResponse(string)


class TLEViewSet(viewsets.ModelViewSet):
    try:
        if(len(TLE.objects.all()) < 1):
            print("Updating TLE data...")
            Services.updateTLE()
            print("...TLE data updated")
    except OperationalError:
        print("Views.TLEViewSet - could not update TLE")
    queryset = TLE.objects.all()
    serializer_class = TLESerializer


class MissionViewSet(viewsets.ModelViewSet):
    try:
        queryset = Mission.objects.all()
        serializer_class = MissionSerializer
    except OperationalError:
        print("MissionViewSet couldn't be loaded yet")


def schedulerQ():
    queue = getSchedulerQ.delay()
    return HttpResponse("Your list: " + queue)


class PyephemData(APIView):

    def get_object(self, pk):
        try:
            return TLE.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tle = self.get_object(pk)
        azel = Services.getAzElTLENow(self, tle)  # pass in object?
        serializer = AZELSerializer(azel)
        return Response(serializer.data)


class MissionsViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


class MissionView(APIView):

    def get(self, request):
        print("WHAT IS THIS SHIT -----------------------===========> GET")
        passes = NextPass.objects.filter(
            setTime__gte=datetime.now()).order_by("riseTime")

        if(len(passes) < 10
                # or len(Mission.objects.all().filter(status="NEW")) > 0
                # or len(Mission.objects.all().filter(status="SCHEDULING")) > 0
                or len(Mission.objects.all()) == 0):
            #scheduler = MOTSimpleHC()
            #scheduler = MOTSteepestHC()
            #scheduler = MOTStochasticHC()
            #scheduler = MOTRandomRestartHC()
            scheduler = MOTRuleBased()
            #scheduler = MOTGA()
            #lis = Services.scheduleMissions(self, missionList, scheduler, 0)
            passes = SchedulerServices.scheduleAndSavePasses(
                self, scheduler, 6)

        serializer = NextPassSerializer(passes, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("WHAT IS THIS SHIT -----------------------===========> POST")
        if Services.makeMissions(request.data):
            name = request.data.get("name")
            pr = request.data.get("priority")
            #ground_station("[" + datetime.now().strftime('%H:%M:%S') + "] " + name + " Priority: " + str(pr))
            scheduler = MOTRuleBased()
            #scheduler = MOTGA()
            #scheduler = MOTSimpleHC()
            SchedulerServices.scheduleAndSavePasses(self, scheduler, 6)
            return HttpResponse(status=201)
        SchedulerServices.scheduleAndSavePasses(self, scheduler, 6)
        return HttpResponse(status=500)

    def delete(self, request, pk):
        print("WHAT IS THIS SHIT -----------------------===========> DELETE")
        print("deleting: " + str(pk))
        missionToDelete = Mission.objects.filter(id=pk)
        deleted = missionToDelete.delete()
        print("Deleted: " + str(deleted))
        # print(missionToDelete[0].name)
        scheduler = MOTRuleBased()
        #scheduler = MOTGA()
        #scheduler = MOTSimpleHC()
        SchedulerServices.scheduleAndSavePasses(self, scheduler, 6)
        return HttpResponse(status=200)


class SchedulerView(APIView):

    def get(self, request):
        isScheduling = False
        if(len(Mission.objects.filter(status="SCHEDULING")) > 0):
            isScheduling = True
        return HttpResponse(isScheduling)


class CSVParseView(APIView):
    """view for exporting as csv"""

    def get(self, request):
        return export_csv(request)

    # def delete(self, request):
    # pass

# where is observer stored AK
# when requesting satellite info, do we use id or name
