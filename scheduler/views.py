from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE, NextPass
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC

from datetime import date,datetime

class TLEList(generics.ListCreateAPIView):
	"""
	With behind the scenes magic, this returns the list of 
	TLEs in the db by serializering the query results, convertng 
	to json and returning it to the place that sent the http request
	"""
	
	some_instance = Services()
	some_instance.updateTLE()# user should be prompted on start up that they need to update the tle
	queryset = get_list_or_404(TLE)
	serializer_class = TLESerializer

class TLEDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	With behind the scenes magic, this returns the details of the
	request TLE from the db by serializering the query result, converting 
	to json and returning it to the place that sent the http request
	"""
	queryset = TLE.objects.all()
	serializer_class = TLESerializer   
# viewset

# class TLEUpdate(APIView):
# 	def post(self, request, format=None):
# 		print("bob") AK
# 		Services.updateTLE()

class PyephemData(APIView):
	"""
	A slightly more exposed verion of APIView, performs
	custom behaviour when a get request is sent
	"""
	def get_object(self, pk):
		try:
			return TLE.objects.get(pk=pk)
		except Snippet.DoesNotExist:
			raise Http404

		
	def get(self, request, pk, format=None):
		"""
		Retrieves the tle data from db, then passes that to other
		functions to get the AzEl object then convers the model
		data into json and returns to http request maker
		"""
		tle = self.get_object(pk)
		azel = Services.getAzElTLENow(self, tle)#pass in object?
		#print(repr(azel.elevation))
		#azel.is_valid() AK

		#Services.makeNextPassDetails(self,tle,30)
		#for x in list:
			#print(x.azimuth)

		serializer = AZELSerializer(azel) 
		return Response(serializer.data)


#where is observer stored AK
#when requesting satellite info, do we use id or name
