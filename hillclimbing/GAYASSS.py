import datetime
import time

class satPass:
	' Class representing passes for satellites'

	def __init__(self, name, startTime, endTime):
		self.name = name
		self.startTime = startTime
		self.endTime = endTime
		self.duration = (endTime.minute- startTime.minute)

magicRainbow = satPass("Vegeta",(datetime.time(9, 0)),(datetime.time(9,20)));
fabbyRainbow = satPass("Goku",(datetime.time(11,0)),(datetime.time(12,20)));
greyRainbow = satPass("Yamcha",(datetime.time(10,10)),(datetime.time(10,30)));
squeakyRainbow = satPass("Goten",(datetime.time(10,40)),(datetime.time(10,50)));

"""
print (magicRainbow.name)
print (magicRainbow.startTime)
print (magicRainbow.endTime)
print(magicRainbow.duration)

print (fabbyRainbow.name)
print (fabbyRainbow.startTime)
print (fabbyRainbow.endTime)
print(fabbyRainbow.duration)
"""

"""
Need a list of orders
iterate through each 
the one with smallest time at end is winner
"""
orderOne = [magicRainbow, fabbyRainbow, greyRainbow, squeakyRainbow]
ordertwo = [squeakyRainbow, fabbyRainbow, greyRainbow, magicRainbow]
orderedPasses = [orderOne, ordertwo]


def fitness():
	""" The smallest time is the winner basically """
	for x in orderedPasses:
		for y,z in zip(x[1:],x):
			print(y.name,z.name)
			print(y.startTime, z.endTime)
			diff=(datetime.datetime.strptime(str(y.startTime),"%I:%M:%S")) - (datetime.datetime.strptime(str(z.endTime),"%I:%M:%S"))
			print("%s" %diff)
fitness()