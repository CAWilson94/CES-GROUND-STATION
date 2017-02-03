#!usr/bin/env python  
from fitnessfunction import FitnessFunction
from datetime import date, datetime, timedelta

def test_findSchedulableSatellites_many_sats():

	sat1AOS = datetime(2017,1,25,12,2,0)
	sat1LOS = datetime(2017,1,25,12,5,0)
	sat2AOS = datetime(2017,1,25,12,0,0)
	sat2LOS = datetime(2017,1,25,12,8,0)
	sat3AOS = datetime(2017,1,25,12,25,0)
	sat3LOS = datetime(2017,1,25,12,30,0)
	sat4AOS = datetime(2017,1,25,11,57,0)
	sat4LOS = datetime(2017,1,25,12,3,0)
	sat5AOS = datetime(2017,1,25,12,7,0)
	sat5LOS = datetime(2017,1,25,12,10,0)
	sat6AOS = datetime(2017,1,25,11,57,0)
	sat6LOS = datetime(2017,1,25,12,4,0)
	sat7AOS = datetime(2017,1,25,11,57,0)
	sat7LOS = datetime(2017,1,25,12,4,0)
	sat8AOS = datetime(2017,1,25,12,59,0)
	sat8LOS = datetime(2017,1,25,13,3,0)
	sat9AOS = datetime(2017,1,25,13,0,0)
	sat9LOS = datetime(2017,1,25,13,4,0)
	sat10AOS = datetime(2017,1,25,12,27,0)
	sat10LOS = datetime(2017,1,25,12,31,0)
	sat11AOS = datetime(2017,1,25,12,28,0)
	sat11LOS = datetime(2017,1,25,12,34,0)

	sat1 = satellite("sat1",sat1AOS, sat1LOS)
	sat2 = satellite("sat2",sat2AOS, sat2LOS)
	sat3 = satellite("sat3",sat3AOS, sat3LOS)
	sat4 = satellite("sat4",sat4AOS, sat4LOS)
	sat5 = satellite("sat5",sat5AOS, sat5LOS)
	sat6 = satellite("sat6",sat6AOS, sat6LOS)
	sat7 = satellite("sat7",sat7AOS, sat7LOS)
	sat8 = satellite("sat8",sat8AOS, sat8LOS)
	sat9 = satellite("sat9",sat9AOS, sat9LOS)
	sat10 = satellite("sat10",sat10AOS,sat10LOS)
	sat11 = satellite("sat11",sat11AOS,sat11LOS)


	#satList=[sat1,sat2,sat3,sat5]
	satList=[sat1,sat2,sat3,sat4,sat5,sat6,sat7,sat8,sat9,sat10,sat11]
		#self.assertIs(shouldBe == ,)


	print(FitnessFunction.fitnessFunction([satList]))


test_findSchedulableSatellites_many_sats()