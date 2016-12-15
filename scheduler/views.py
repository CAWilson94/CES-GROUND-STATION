from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from scheduler.services import services
from scheduler.models import TLE
import requests

def index(request):

	#sessionObject = requests.Sessions()
	#sessionObject.mount('https://celestrak.com',myAdapter())
	#sessionObject.get...
	tle_list = services.updateTLE()
	
	#tle_list = TLE.objects.all()
	print (tle_list)
	string = "Display satellites"
	context_dict = {'message':tle_list,
				}

	return render(request, 'scheduler/index.html', context_dict)
# Create your views here.
