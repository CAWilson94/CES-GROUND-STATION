import requests
from scheduler.models import TLE

class services():

	def updateTLE():
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle=0
		tle = requestsObject.text
		
		#check format is as expected?
		splitByBothList = services.splitTLE(tle)
		
		final = services.filterTLE(splitByBothList)

		i=0
		while i != (len(final)-3):
			#print (final)
			try: 
				tleentry = TLE.objects.get(name=final[i])
				pass
			except TLE.DoesNotExist:
				#create new entry in db
				newTLE = TLE(name = final[i], line1 = final[i+1], line2 = final[i+2])
				newTLE.save()
			else:
				#update existing
				tleentry.line1 = final[i+1]
				tleentry.line2 = final[i+2]
			i+=3

		return (splitrnTLEList)

	#add up name or line array to single space delimited string
	def adder(stringsep):  #nicer way?
		string=""
		for x in stringsep:
			string = string+x+" "
		return (string)

	def splitTLE(rawTLE):
		splitrnTLEList = rawTLE.split('\r\n')

		cookedTLE = []
		for x in splitrnTLEList:
			cookedTLE.append(x.split(" "))
		return (cookedTLE)

	def filterTLE(rawTLE):
				#filter out the empty entries caused by splitting '       '
		newLineOrNameList=[]
		filteredTLE=[]
		for lineOrNameList in rawTLE:
			newLineOrNameList = [lineOrName for lineOrName in lineOrNameList if lineOrName!='']
			filteredTLE.append(services.adder(newLineOrNameList))

		#delete odd empty end entry 
		if filteredTLE[len(filteredTLE)-1]=='':
			del filteredTLE[len(filteredTLE)-1]  #nicer way?
		return (filteredTLE)