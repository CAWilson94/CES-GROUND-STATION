from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from scheduler.services import services
from scheduler.models import TLE
import requests

def index(request):

	#secure way
	#sessionObject = requests.Sessions()
	#sessionObject.mount('https://celestrak.com',myAdapter())
	#sessionObject.get...

	#updates on refresh cause buttons require something extra like js...
	tle_list = services.updateTLE()
	print (tle_list)
	#gets all db entries
	tle_list1 = TLE.objects.all()
	
	context_dict = {'tle_list':tle_list1,
				}

	return render(request, 'scheduler/index.html', context_dict)
# Create your views here.
