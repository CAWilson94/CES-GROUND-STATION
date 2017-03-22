from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer,ChosenSatSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route
from rest_framework.renderers import StaticHTMLRenderer


class TLEViewSet(viewsets.ModelViewSet):
	Services.updateTLE()
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
		#print(repr(azel.elevation))
		#azel.is_valid() AK

		#Services.makeNextPassDetails(self,tle,30)
		#for x in list:
			#print(x.azimuth)

		serializer = AZELSerializer(azel)
		return Response(serializer.data)

class Mission(APIView):
	def post(self,request):
		chosenSatsList = request.POST.getlist('name')		
		if Services.makeMissions(chosenSatsList):
			return HttpResponse(status=201)
		return HttpResponse(status=404)

	# def delete(self, request):
	# 	pass
#where is observer stored AK
#when requesting satellite info, do we use id or name
