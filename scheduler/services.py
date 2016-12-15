import requests
from scheduler.models import TLE

class services():

	def adder(stringsep):
		string=""
		for x in stringsep:
			string = string+x+" "
		return (string)

	def updateTLE():
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle = requestsObject.text
		splitTLE = tle.split(" ")

		while len(splitTLE) != 0:
			namesep = []
			while splitTLE[0]!="1":
				namesep.append(splitTLE.pop(0))
				
			name = adder(namesep)

			line1sep = splitTLE[:9]
			del splitTLE[:9]
			line1 = adder(line1sep)

			line2sep = splitTLE[:8]
			del splitTLE[:8]
			line2 = adder(line2sep)

			newTLE = TLE(name=name,line1=line1,line2=line2)
			newTLE.save()


