import datetime
import time
import random

CROSSOVER_RATE = 10; # TODO: Ammend this

class satPass:
	' Class representing passes for satellite passes'
	def __init__(self, name, startTime, endTime):
		self.name = name
		self.startTime = startTime
		self.endTime = endTime
		self.duration = (endTime.minute- startTime.minute)


class Individual:
	' Class representing an individual (or chromosome)'
	def __init__(self, satList, fitness):
		self.satList = satList
		self.fitness = fitness

	def setSatList(satList):
		self.satList = satList

	def setFitness(fitness):
		self.fitness = fitness
# Just some test data ... nothing to see here.
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
orderedPasses = [orderOne, ordertwo] # More test data .. more of nothing to see here.


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


# May need to create class to package together the indiviuals. Or rather, map from db to object. 
# This should be done with Django however. 
indiOne = Individual(orderOne,fitness(orderOne))
indiTwo = Individual(ordertwo, fitness(ordertwo))

indiList = [indiOne,indiTwo] # TODO: This and the above should be in createPopulation? 

def createPopulation(indiList): # will replace with db 
	"""will take in data from db instead and package individuals from there"""
	population = []
	for item in indiList:
		population.append(item)
	return population

def randomParents(population):
	""" Select Parents for tournament function"""
	tempList = []
	parents = []
	for index in range(2):
		parentOne = random.randint(0,len(population))
		parentTwo = random.randint(0,len(population))
		tempList.extend([parentOne,parentTwo])
		sortByFitness(tempList)
		parents.append(tempList[0])
		clear(tempList)
	retun parents

def tournie(population):
	"""Tournament to generate new generation"""
	newGen = []
	crossed = []
	while(len(crossed)!=len(population)):
		newGen = randomParents(population) # TODO: create randomParents function
		i = random.randint(0,10) # Random int between 0 and 10
		if(i < CROSSOVER_RATE):
			tempIndiList = crossover(newGen[0], newGen[1])
			crossed.extend(tempIndiList)
			clear(newGen)
	return crossed

def clear(someList):
	"""python does not seem to have a clear list function..
		Splice in the list [] (0 elements) at the location [:]
		(all indexes from start to finish)
	"""
	someList[:] = []


def GA(population):
	""" Genetic algorithm for finding best suited order of sats """
	population = createPopulation(population)
	best = [] # Keep a list of the recent best solutions
	gen = 0;
	while(true):
		gen++
		sortByFitness(population)
		population.append(best[0])
		if(gen > 100): # since there is no definitive stopping value. i.e. if fitness was 0
			sortByFitness(best)
			print("best order is: " + best[0])
			return
	print("generation: " + gen + "best: " + population[0].chromosomeString) # TODO: create this chromosome string getter for population 
	population = tournie(population) # TODO: Create tournie function		



GA(createPopulation(indiList))


