import requests
from scheduler.models import TLE
import ephem
class services():

	#Retrieving TLE data from external source and placing in the db 
	def updateTLE():
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle=requestsObject.text
		
		#check format is as expected?

		#split leaves one list with format
		#name, line1, line2, name, line1, line2
		final = tle.split('\r\n')
	
		#remove errant empty entry
		if final[len(final)-1]=='':
		 	del final[len(final)-1] 

		#call post in here
		i=0
		while i != (len(final)-3):
			name = services.adder(final[i]).strip()
			try: 
				tleentry = TLE.objects.get(name=name)
				pass
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name =name, line1 = final[i+1], line2 = final[i+2])
				newTLE.save()
			else:
				#update existing
				tleentry.line1 = final[i+1]
				tleentry.line2 = final[i+2]
				tleentry.save()
			i+=3	

	#add up name or line array to single space delimited string
	def adder(stringsep):  #nicer way?
		string=""
		for x in stringsep:
			string = string+x
		return (string)