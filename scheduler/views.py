from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE, NextPass
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer,ChosenSatSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC
from rest_framework.decorators import detail_route
from rest_framework.renderers import StaticHTMLRenderer

from datetime import date,datetime

class TLEViewSet(viewsets.ModelViewSet):
	Services.updateTLE()
	queryset = TLE.objects.all()
	serializer_class = TLESerializer

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

class postEx(APIView):

	def post(self,request):

		# serializer = ChosenSatListSerializer(data=request.data)
		# if serializer.is_valid():
		# 	serializer.save()
		# 	return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		# return Response(serializer.data,status=status.HTTP_201_CREATED)
#http://stackoverflow.com/questions/28010663/serializerclass-field-on-serializer-save-from-primary-key
		
		
		listing = request.POST.getlist('name[]')
		print(listing)
		print ("blah")
		
		for elem in listing:
			print(elem)
			serializer = ChosenSatSerializer(data=elem)
			if serializer.is_valid():
				pass
			#	serializer.save()
			# 	print("if")
			# else:
			# 	return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		
		return Response(serializer.data,status=status.HTTP_201_CREATED)
	#return HttpResponseRedirect(reverse())

#where is observer stored AK
#when requesting satellite info, do we use id or name
