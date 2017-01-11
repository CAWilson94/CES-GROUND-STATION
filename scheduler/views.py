from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from scheduler.models import TLE
from scheduler.services import services
from scheduler.serializers import CubeSatSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_list_or_404


class TLEList(APIView):
	"""
    List all TLE, or create a new TLE.
    """
	def get(self, request, format=None):

		services.updateTLE()
		TLEList = TLE.objects.all()
		serializer = CubeSatSerializer(TLEList, many=True)#, many=True
		return Response(serializer.data)


	def post(self, request, format=None):
		serializer = SubeSatSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)