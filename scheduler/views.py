from django.http import HttpResponse
from django.db.utils import OperationalError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE, Mission
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer, MissionSerializer, NextPassSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.renderers import StaticHTMLRenderer
from csv_parse import export_csv

from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.stochasticHC import MOTStochasticHC
from scheduler.MOT.randomRestartHC import MOTRandomRestartHC


class TLEViewSet(viewsets.ModelViewSet):
    try:
        Services.updateTLE()
    except OperationalError:
        print("Views.TLEViewSet - could not update TLE")
    queryset = TLE.objects.all()
    serializer_class = TLESerializer


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
        missions = Mission.objects.all()
        missionList = []
        for mission in missions:
            missionList.append(mission)
        # print(missionList)
        scheduledMissionList = Services.scheduleMissions(self, missionList, MOTSimpleHC)
        #print("final List: {}".format(lis))
        scheduledMissionList.sort(key=lambda r: r.riseTime)
        
        serializer = NextPassSerializer(scheduledMissionList, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        if Services.makeMissions(request.data):
            content = {'data accepted': 'saved to DB'}
            return Response(content, status=status.HTTP_202_ACCEPTED)

        content = {'data accepted': "but couldn't save to DB"}   
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CSVParseView(APIView):
    """view for exporting as csv"""

    def get(self, request):
        return export_csv(request)

    # def delete(self, request):
    # pass

# where is observer stored AK
# when requesting satellite info, do we use id or name
