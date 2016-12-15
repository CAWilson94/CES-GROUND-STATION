from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from scheduler.services import services
from scheduler.models import TLE

def index(request):

	#sessionObject = requests.Sessions()
	#sessionObject.mount('https://celestrak.com',myAdapter())
	#sessionObject.get...
	services.updateTLE()
	
	tle_list = TLE.objects.all()
	string = "Display satellites"
	context_dict = {'tle_list':tle_list,
				}

	return render(request, 'scheduler/index.html', context_dict)
# Create your views here.
