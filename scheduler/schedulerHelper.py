from datetime import datetime, timedelta
from scheduler.services import Services
from scheduler.models import TLE, Mission, NextPass


class SchedulerHelper():

	TIME_HOURS = 72

	def getPassesFromMissions(self, missions):
		passes = []

		dateNow = datetime.utcnow()

		print("Total missions: " + str(len(missions)))
		i = 0
		for mission in missions:
			i += 1

			tleEntry = mission.TLE
			try:
				nextPass = Services.getNextPass(self, tleEntry, mission, dateNow)
				passes.append(nextPass)
			
				while(nextPass.setTime < (dateNow + timedelta(hours=SchedulerHelper.TIME_HOURS))):
					time = nextPass.setTime + timedelta(minutes=1)
					try:
						nextPass = Services.getNextPass(self, tleEntry, mission, time)
						passes.append(nextPass)
						
					except ValueError: 
						break

				print("Finding passes for the next 36 hours, found: " + str(len(passes)) + ", now looking at " + str(i) + " : " + mission.TLE.name)
			except ValueError: 
				print("No pass was found for " + tleEntry.name + " over groundstation in the next 36 hours.")
		return passes