from datetime import datetime, timedelta
from scheduler.services import Services
from scheduler.models import TLE, Mission, NextPass


class SchedulerHelper():

	def getPassesFromMissions(self, missions):
		passes = []

		dateNow = datetime.now()

		print("Total missions: " + str(len(missions)))
		i = 0
		for m in missions:
			i += 1
			print("Finding passes for the next 36 hours, found: " + str(len(passes)) + ", now looking at " + str(i) + " : " + m.TLE.name)

			tleEntry = m.TLE
			try:
				nextPass = Services.getNextPass(self, tleEntry, m, dateNow)
				passes.append(nextPass)
			
				while(nextPass.setTime < (dateNow + timedelta(hours=36))):
					time = nextPass.setTime + timedelta(minutes=1)
					try:
						nextPass = Services.getNextPass(self, tleEntry, m, time)
						passes.append(nextPass)
						
					except ValueError: 
						break
			except ValueError: 
					print("No pass was found for " + tleEntry.name + " over groundstation in the next 36 hours.")
		return passes