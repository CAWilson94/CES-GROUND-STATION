

from django.shortcuts import render
from django.http import HttpResponse

def index(request):

	context_dict = {'message':"Display satellites"}

	return render(request, 'scheduler/index.html', context_dict)
# Create your views here.
