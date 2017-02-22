import datetime
import time

class satPass:
	' Class representing passes for satellites'

	def __init__(self, name, startTime, endTime):
		self.name = name
		self.startTime = startTime
		self.endTime = endTime
		self.duration = (endTime.minute- startTime.minute)


class Individual:
	' Class representing an individual'
	def __init__(self, satList, fitness):
		self.satList = satList
		self.fitness = fitness

	def setSatList(satList):
		self.satList = satList

	def setFitness(fitness):
		self.fitness = fitness

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


def fitness(passList):
	""" The smallest time is the winner basically """
	total = 0;
	for y,z in zip(passList[1:],passList):
		#print(y.name,z.name)
		#print(y.startTime, z.endTime)
		diff=(datetime.datetime.strptime(str(y.startTime),"%I:%M:%S")) - (datetime.datetime.strptime(str(z.endTime),"%I:%M:%S"))
		#print("%s" %diff)
		total += abs(int(diff.total_seconds()))
	fitness = total;
	y.fitness = fitness # want fitness to be for the orders so create individual from this
	return fitness



indiOne = Individual(orderOne,fitness(orderOne))
indiTwo = Individual(ordertwo, fitness(ordertwo))

indiList = [indiOne,indiTwo]

def createPopulation(indiList): # will replace with db 
	'will take in data from db instead and package individuals from there' 
	population = []
	for item in indiList:
		population.append(item)
	return population


def GA(population):
	for item in population:
		print("fitness is:")
		print(item.fitness)


GA(createPopulation(indiList))


