from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from scheduler.services import services
from scheduler.models import TLE
import requests
from django.views import generic
from django.shortcuts import render, redirect



def index(request):

	#secure way
	#sessionObject = requests.Sessions()
	#sessionObject.mount('https://celestrak.com',myAdapter())
	#sessionObject.get...

	#updates on refresh cause buttons require something extra like js...
	#tle_list = services.updateTLE()

	#gets all db entries
	tle_list1 = get_list_or_404(TLE)
	
	epoch = services.ephem()
	#print (epoch)

	context_dict = {'epoch':epoch,
					'tle_list':tle_list1,
				}

	return render(request, 'scheduler/index.html', context_dict)

# class IndexView(generic.ListView):
# 	template_name = 'scheduler/index.html'
# 	context_object_name =  'tle_list'

# 	def get_queryset(self):
# 		return get_list_or_404(TLE)

def updateTLE1(request):
	print("blah2.0")
	tle_list = services.updateTLE()
	
	context_dict = {'epoch':"none",
	 				'tle_list':tle_list,
	 			}
	
	return redirect('/scheduler/')
	#return render(request, 'scheduler/index.html', context_dict)

# Create your views here.
