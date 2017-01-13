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

class TLEDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = TLE.objects.all()
	serializer_class = TLESerializer   
# viewset

# class TLEUpdate(APIView):
# 	def post(self, request, format=None):
# 		print("bob")
# 		services.updateTLE()


