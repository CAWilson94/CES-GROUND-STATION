from django.http import HttpResponse
from django.db.utils import OperationalError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE, Mission
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer, MissionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.renderers import StaticHTMLRenderer


class TLEViewSet(viewsets.ModelViewSet):
	try:
		#Services.updateTLE()
		pass
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
		azel = Services.getAzElTLENow(self, tle)#pass in object?
		serializer = AZELSerializer(azel)
		return Response(serializer.data)

class MissionView(APIView):

	def get(self,request):
		missions = Mission.objects.all()
		serializer = MissionSerializer(missions,many=True)
		return Response(serializer.data)

	def post(self,request):
		print(request.data)
		for elem in request.data:
			print (elem)
		print("something happened")	
		if Services.makeMissions(request.data):
			return HttpResponse(status=201)
		return HttpResponse(status=500)

	# def delete(self, request):
	# 	pass
#where is observer stored AK
#when requesting satellite info, do we use id or name
