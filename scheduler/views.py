from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE
from scheduler.services import Services
from scheduler.serializers import TLESerializer, AZELSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view


class TLEList(generics.ListCreateAPIView):

	Services.updateTLE()
	queryset = get_list_or_404(TLE)
	serializer_class = TLESerializer

class TLEDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = TLE.objects.all()
	serializer_class = TLESerializer   
# viewset

# class TLEUpdate(APIView):
# 	def post(self, request, format=None):
# 		print("bob")
# 		Services.updateTLE()

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
		#azel.is_valid()

		#Services.makeNextPassDetails(self,tle,30)
		#for x in list:
			#print(x.azimuth)

		serializer = AZELSerializer(azel)
		return Response(serializer.data)


#where is observer stored
#when requesting satellite info, do we use id or name

#how does get get the 