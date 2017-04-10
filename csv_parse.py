from scheduler.models import Mission, NextPass
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv


def export_csv(request):
    queryset = NextPass.objects.all() 
    response = HttpResponse(content_type='text/csv') #should probs be REST response 
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # To open UTF-8 properly
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"Rise Time"),
        smart_str(u"Set Time"),
        smart_str(u"Duration"),
    ])


    for object in queryset:
        writer.writerow([
            smart_str(object.tle.name),
            smart_str(object.riseTime),
            smart_str(object.setTime),
            smart_str(object.duration),
        ])

    return response
