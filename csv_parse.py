from scheduler.models import Mission
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv


def export_csv():
    queryset = Mission.objects.all()
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

    writer = csv.writer(csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # To open UTF-8 properly
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"Status"),
        smart_str(u"Priority"),
    ])

    print("done this...")

    for object in queryset:
        writer.writerow([
            smart_str(object.name),
            smart_str(object.status),
            smart_str(object.priority),
        ])

    return response
