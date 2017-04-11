"""
Created on 31 March 2017
@author: Charlotte Alexandra Wilson

Last revision: 05 April 2017
---------------------------------------------------------------
Testing various constants and variables for scheduler output
"""

import datetime
import time
import csv
from scheduler.models import Mission, NextPass


def test(passes, run_time):

    csv_name = "scheduler_compare.csv"
    resultFile = csv.writer(open(csv_name, 'a', newline=''))

    first_pass = passes.first().riseTime
    print("FIRST PASS: " + str(first_pass))
    end_pass = passes.last().setTime
    print("END PASS: " + str(end_pass))

    duration = end_pass - first_pass

    mission = Mission.objects.all()
    num_missions = len(mission)

    total_contact_time_seconds = 0
    for item in passes:
        if item.duration is not None:
            total_contact_time_seconds += item.duration.seconds

    """convert total contact time to date time object """
    total_contact_time_int = datetime.timedelta(
        seconds=total_contact_time_seconds)
    total_non_contact_time = duration - total_contact_time_int

    contact_time_percentage = str(round(
        ((total_contact_time_int / duration) * 100), 2)) + "%"

    resultFile.writerow(
        [num_missions, duration, total_contact_time_int,
         total_non_contact_time, contact_time_percentage , str(run_time)])

    print("TOTAL DURAITON: " + str(duration) +
          "=======================================")
    print("TOTAL CONTACT TIME: " + str(total_contact_time_int) +
          "=======================================")
    print("TOTAL NON CONTACT TIME: " + str(total_non_contact_time) +
          "=======================================")
    print("CONTACT TIME PERCENTAGE: " + str(contact_time_percentage) +
          "=======================================")