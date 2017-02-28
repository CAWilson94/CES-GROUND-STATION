"""
Currently population works by just adding in a list of chromosomes
Need to figure out how to get fitness of a chromosome

"""


import datetime
import time
import random
import operator

CROSSOVER_RATE = 10; # TODO: Ammend this
FITNESS_CMP= operator.attrgetter("fitness")
START_TIME_CMP= operator.attrgetter("startTime")

class satPass:
    ' Class representing passes for satellite passes: which in turn, represents a gene in a chromosome'
    def __init__(self, name, startTime, endTime):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.duration = (endTime.minute- startTime.minute)

class Population:
    ' Class representing population: a population contains chromosomes hurrah!'

    def __init__(self, chromosome):
        self.chromosome = chromosome

class Chromosome:
    ' Class representing a chromosome: where a chromosome is basically a random ordered list of sat passes'
    fitness = 0;
    def __init__(self, satPassList):
        self.satPassList = satPassList
        #self.fitness = fitness # update later

def crossover():
 """crossover function"""



def randomParents(population):
    """ Select Parents for tournament function"""
    tempList = []
    parents = []
    #for index in range(2):
    parentOne = random.randint(0,len(population))
    for item in parentOne:
       	print("P1: " +  item)
        #parentTwo = random.randint(0,len(population))
        #tempList.extend([parentOne,parentTwo])
        #sortByFitness(tempList)
        #parents.append(tempList[0])
        #clear(tempList)
    #return parents


def fitness(chromosome):
    """ The smallest time is the winner basically """
    total = 0;
    for y,z in zip(chromosome.satPassList[1:],chromosome.satPassList):
        #print(y.name,z.name)
        #print(y.startTime, z.endTime)
        diff=(datetime.datetime.strptime(str(y.startTime),"%I:%M:%S")) - (datetime.datetime.strptime(str(z.endTime),"%I:%M:%S"))
        #print("%s" %diff)
        total += abs(int(diff.total_seconds()))
    fitness = total;
    y.fitness = fitness # want fitness to be for the orders so create individual from this
    return fitness

def tournie(population):
    """Tournament to generate new generation"""
    newGen = []
    crossed = []
    while(len(crossed)!=len(population)):
        newGen = randomParents(population)
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

def sortByFitness(population):
    "sort chromosomes by fitness"
    fitnessSorted = sorted(population, key=FITNESS_CMP)
    return fitnessSorted

   
def GA(population):
    """ Genetic algorithm for finding best suited order of sats """
    best = [] # Keep a list of the recent best solutions
    gen = 0;
    while(1):
        gen+=1
        population = sortByFitness(population)
        best.append(population[0])
        if(gen > 100): # since there is no definitive stopping value. i.e. if fitness was 0
            best = sortByFitness(best)
            print("best fitness: %s" %best[0].fitness)
            print("best order is:")
            for item in best[0].satPassList:
            	print(item.name)
            return
        tournie(population)
    print("generation: " + gen + "best: " + population[0].chromosomeString) # TODO: chromosomeString should be Gene string.


' ---------------------- Testing Data ---------------------- '
# Each one of these is a gene

magicRainbow = satPass("Vegeta",(datetime.time(9, 0)),(datetime.time(9,20)));
fabbyRainbow = satPass("Goku",(datetime.time(11,0)),(datetime.time(12,20)));
greyRainbow = satPass("Yamcha",(datetime.time(10,10)),(datetime.time(10,30)));
squeakyRainbow = satPass("Goten",(datetime.time(10,40)),(datetime.time(10,50)));


orderOne = [magicRainbow, fabbyRainbow, greyRainbow, squeakyRainbow] # A chromosome basically (or individual)

chromo1 = sorted(orderOne, key= START_TIME_CMP)

for item in chromo1:
	print(item.name)

"""
population = orderedPasses

for chromosome in population:
	for gene in chromosome:
		print(gene.name)



""
chromo1.fitness = fitness(chromo1)
chromo2.fitness = fitness(chromo2)

chromoList = [chromo1,chromo2]

"""
"""



for item in chromoList:
	print(item.fitness)

chromoList = sortByFitness(chromoList)

print("now sorted by fitness: \n")

for item in chromoList:
	print(item.fitness)
"""

"""
Testing tounie now:
	RandomParents issue: 
		For random parents you will need to look through the sat passes list (or DB)
		select random sat passes to fill each chromosome..

		Clearly, the number of passes in each chromosome can be different, so how do we decide this?

"""

"""
print("\nmother\n")
for item in chromo1.satPassList:
	print(item.name)

print("\nfatherz\n")
for item in chromo2.satPassList:
	print(item.name)

population = chromoList

mother = population[0].satPassList
father = population[1].satPassList

child = mother[:3] + father[3:]

childChromo = Chromosome(child)
childChromo.fitness = fitness(childChromo)

print("\nchild\n")
for item in childChromo.satPassList: 
	print(item.name)
	
"""

# Need to make sure the lists are always unique and not repeating elements?







