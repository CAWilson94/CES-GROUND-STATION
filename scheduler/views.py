from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE
from scheduler.services import services
from scheduler.serializers import TLESerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view


class TLEList(generics.ListCreateAPIView):
	services.updateTLE()
	queryset = get_list_or_404(TLE)
	serializer_class = TLESerializer

class TLEDetail(APIView):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	def get_object(self, pk):
		try:
			return TLE.objects.get(pk=pk)
		except TLE.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		tle = self.get_object(pk)		
		print(tle)
		serializer = TLESerializer(tle)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		tle = self.get_object(pk)	
		serializer = TLESerializer(tle, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		tle = self.get_object(pk)	
		tle.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

# class TLEDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = get_list_or_404(TLE)
# 	serializer_class = TLESerializer   
#This should work but it doesn't
#viewset

 


