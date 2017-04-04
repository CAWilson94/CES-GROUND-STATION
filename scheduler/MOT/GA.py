"""
Created on 6 Feb 2017
@author: Charlotte Alexandra Wilson

Last revision: 28 March 2017
---------------------------------------------------------------


Objects Description:
---------------------------------------------------------------
Population: list of Chromosome Objects
Chromosome:
    Attributes:
        satPassList     A list of satellite pass objects
        fitness         The fitness of the chromosome
SatPass:
    Attributes:
        name:           Name of the satellite from TLE data (changing to TLE.name from next pass model)
        startTime:      Start time of sat pass (RiseTime from next pass model)
        endTime:        End time of sat pass (SetTime from next pass model)
        duration:       Duration of sat pass ( duration from next pass model)

"""

import datetime
import random
import operator
from random import randint

CROSSOVER_RATE = 7
FITNESS_CMP = operator.attrgetter("fitness")
START_TIME_CMP = operator.attrgetter("startTime")
RISE_TIME_CMP = operator.attrgetter("riseTime")
CHROMO_LENGTH = 10
POPULATION_SIZE = 10
passNames = ["cube_a", "cube_b", "cube_c", "cube_d"]


class satPass:
    """ Class representing passes for satellite passes: which in turn, represents a gene in a chromosome

        Attributes:
            name:           Name of the satellite from TLE data (changing to TLE.name from next pass model)
            startTime:      Start time of sat pass (RiseTime from next pass model)
            endTime:        End time of sat pass (SetTime from next pass model)
            duration:       Duration of sat pass ( duration from next pass model)

    """

    def __init__(self, name, startTime, endTime):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.duration = (endTime.minute - startTime.minute)


class Chromosome:
    """ Class representing a chromosome: where a chromosome is basically a random ordered list of sat passes

        Attributes:
        satPassList     A list of satellite pass objects
        fitness         The fitness of the chromosome

    """
    fitness = 0

    def __init__(self, satPassList):
        self.satPassList = satPassList
        # self.fitness = fitness # update later


' ---------------------- Testing Data ---------------------- '
cube_a = satPass("cube_a", (datetime.datetime(2017, 12, 4, 9, 0)),
                 (datetime.datetime(2017, 12, 4, 10, 0)))
cube_b = satPass("cube_b", (datetime.datetime(2017, 12, 4, 9, 20)),
                 (datetime.datetime(2017, 12, 4, 9, 40)))
cube_c = satPass("cube_c", (datetime.datetime(2017, 12, 4, 10, 20)),
                 (datetime.datetime(2017, 12, 4, 10, 40)))
cube_d = satPass("cube_d", (datetime.datetime(2017, 12, 4, 11, 0)),
                 (datetime.datetime(2017, 12, 4, 11, 20)))
cube_e = satPass("cube_e", (datetime.datetime(2017, 12, 4, 11, 10)),
                 (datetime.datetime(2017, 12, 4, 11, 40)))
cube_f = satPass("cube_f", (datetime.datetime(2017, 12, 4, 11, 30)),
                 (datetime.datetime(2017, 12, 4, 11, 50)))
cube_g = satPass("cube_g", (datetime.datetime(2017, 12, 4, 12, 0)),
                 (datetime.datetime(2017, 12, 4, 12, 30)))


cube_h = satPass("cube_h", (datetime.datetime(2017, 12, 4, 10, 0)),
                 (datetime.datetime(2017, 12, 4, 11, 0)))
cube_i = satPass("cube_i", (datetime.datetime(2017, 12, 4, 10, 20)),
                 (datetime.datetime(2017, 12, 4, 10, 40)))
cube_j = satPass("cube_j", (datetime.datetime(2017, 12, 4, 11, 20)),
                 (datetime.datetime(2017, 12, 4, 11, 40)))
cube_k = satPass("cube_k", (datetime.datetime(2017, 12, 4, 11, 0)),
                 (datetime.datetime(2017, 12, 4, 12, 20)))
cube_l = satPass("cube_l", (datetime.datetime(2017, 12, 4, 12, 10)),
                 (datetime.datetime(2017, 12, 4, 12, 40)))
cube_m = satPass("cube_m", (datetime.datetime(2017, 12, 4, 12, 30)),
                 (datetime.datetime(2017, 12, 4, 12, 50)))
cube_n = satPass("cube_n", (datetime.datetime(2017, 12, 4, 13, 0)),
                 (datetime.datetime(2017, 12, 4, 13, 30)))

TEST_PASS_LIST = [cube_a, cube_d, cube_b, cube_e, cube_f, cube_c, cube_g, cube_h,
                  cube_i, cube_j, cube_k, cube_l, cube_m, cube_n]


def crossover(chromoOne, chromoTwo):
    """crossover function: crosses over pass lists while keeping them in order wrt to time."""
    child1satPassList = chromoOne.satPassList[:2] + chromoTwo.satPassList[2:]
    child2satPassList = chromoTwo.satPassList[:2] + chromoOne.satPassList[2:]

    childOne = Chromosome(child1satPassList)
    childTwo = Chromosome(child2satPassList)
    # Could probably create a "package Chromosome" function..
    childOne.fitness = nextPassFitness(childOne)
    childTwo.fitness = nextPassFitness(childTwo)
    childOne.satPassList = sorted(childOne.satPassList, key=RISE_TIME_CMP)
    childTwo.satPassList = sorted(childTwo.satPassList, key=RISE_TIME_CMP)
    childList = [childOne, childTwo]

    return childList


def randomParents(population):
    """ Select Parents for tournament function"""
    tempList = []
    parents = []
    for index in range(1):
        # Two random int's from range 0 - population length
        randomint = random.sample(range(len(population)), 2)

        tempList.append(population[randomint[0]])  # A single chromosome
        tempList.append(population[randomint[1]])  # A single chromosome
        # Do not really need sort by fitness..
        tempfit = setFitness(tempList)
        temp = sortByFitness(tempfit)

        # List with two chromosomes randomly picked from the current population
        parents = temp  # A list with two
        # printPopulation(parents)
        # Clear lists for next cal
        tempList = []
        tempfit = []
        temp = []
    return parents


def setFitness(population):
    """ set fitness of every chromosome in population so this is only done once in the program: 
        i.e. instead of setting fitness on chromosome creation and crossover just do it in the 
        GA function.

        returns a population of chromosomes with fitnesses :O 
    """
    for chromosome in population:
        chromosome.fitness = nextPass_fitnessVariety_sum(chromosome)

    return population


def fitness(chromosome):
    """ The smallest time is the winner basically """
    total = 0
    for y, z in zip(chromosome.satPassList[1:], chromosome.satPassList):
        # print(y.name,z.name)
        # print(y.startTime, z.endTime)
        diff = (y.startTime - z.endTime)
        # diff=(datetime.datetime.strptime(str(y.startTime),"%H:%M:%S")) - (datetime.datetime.strptime(str(z.endTime),"%H:%M:%S"))
        # print("%s" %diff)
        total += abs(int(diff.total_seconds()))
    fitness = total
    y.fitness = fitness  # want fitness to be for the orders so create individual from this
    return fitness


def nextPassFitness(chromosome):
    """
    Fitness specific to nextpass lists
    """
    total = 0
    for y, z in zip(chromosome.satPassList[1:], chromosome.satPassList):
        diff = (y.riseTime - z.setTime)
        total += abs(int(diff.total_seconds()))
    fitness = total
    y.fitness = fitness
    return fitness


def fitnessPassSum(chromosome):
    """ Here, the metric for fitness is going to be most contact with sats: so bigger is better"""
    fitness = 0
    for satPass in chromosome.satPassList:
        fitness += (satPass.endTime - satPass.startTime)
    return fitness


def fitnessVariety_sum(chromosome):
    """  want different sats and not just any.. """
    diffNames = 0
    satLookedat = []
    duration = 0
    for satPass in chromosome.satPassList:
        duration += (satPass.endTime - satPass.startTime).total_seconds()
        # print(satPass.name, " duration: ", duration)
        if satPass.name not in satLookedat:
            satLookedat.append(satPass.name)
            diffNames += 1

    # print(diffNames, "diffNames: ", diffNames)
    fitness = duration * diffNames
    # print("fitness: ", fitness)
    return fitness


def nextPass_fitnessVariety_sum(chromosome):
    """  want different sats and not just any.. """
    diffNames = 0
    satLookedat = []
    duration = 0
    for satPass in chromosome.satPassList:
        duration += (satPass.setTime - satPass.riseTime).total_seconds()
        # print(satPass.name, " duration: ", duration)
        if satPass.tle.name not in satLookedat:
            satLookedat.append(satPass.tle.name)
            diffNames += 1

    # print(diffNames, "diffNames: ", diffNames)
    fitness = duration * diffNames
    # print("fitness: ", fitness)
    return fitness


def tournie(population):
    """Tournament to generate new generation"""
    newGen = []
    crossed = []
    i = 0
    while len(crossed) != len(population):
        newGen = randomParents(population)
        # printPopulation(newGen)
        i = random.randint(0, 7)
        if i < CROSSOVER_RATE:
            #print("crossing over!")
            tempIndiList = crossover(newGen[0], newGen[1])
            # printPopulation(tempIndiList)
            crossed.extend(tempIndiList)
            # printPopulation(crossed)
            newGen = []

    return crossed


def sortByFitness(population):
    "sort chromosomes by fitness"
    fitnessSorted = sorted(population, key=FITNESS_CMP)
    return fitnessSorted


def conflictSingle(satPassB, passAendTime):
    if (satPassB.riseTime < passAendTime):
        return True
    else:
        return False


def randomChromosome(chromosome):
    """ Generates random chromosome with random non conflicting sat passes: i.e. picks from conflicting windows"""
    conflictList = []
    chromosome = chromosome.satPassList
    orderedPassList = []
    i = 0

    d = {}

    while i < len(chromosome):
        windowEnd = chromosome[i].setTime

        for j in range(i + 1, len(chromosome)):

            if (conflictSingle(chromosome[j], windowEnd)):
                if chromosome[i] not in conflictList:
                    conflictList.append(chromosome[i])

                if chromosome[j] not in conflictList:
                    conflictList.append(chromosome[j])

                if chromosome[j].setTime > chromosome[i].setTime:
                    windowEnd = chromosome[j].setTime
            else:

                if (conflictList):
                    d[len(orderedPassList)] = conflictList
                    orderedPassList.append(
                        conflictList[randint(0, len(conflictList) - 1)])
                else:
                    orderedPassList.append(chromosome[i])

                conflictList = []
                i = j - 1
                break
        if (i == len(chromosome) - 1):
            orderedPassList.append(chromosome[i])
        i += 1

    """
    print("\nRandom chromosome")

    for item in orderedList:
        print(item.name)

    print("Dictionary: \n")

    for k, v in d.items():

        stringName = ""
        for item in v: 
            stringName+=item.name + " "

        print(k,stringName)
        """
    randomChromosome = Chromosome(orderedPassList)
    # randomChromosome.fitness = fitness(randomChromosome)

    return randomChromosome


def genPasses():
    randNames = randint(0, len(passNames) - 1)
    name = passNames[randNames]
    rstartmin = randint(0, 59)
    rstartHour = randint(0, 23)
    rendmin = randint(0, 59)
    rendHour = randint(0, 23)
    startTime = (datetime.time(rstartHour, rstartmin))
    endTime = (datetime.time(rendHour, rendmin))
    return satPass(name, startTime, endTime)


def generateChromosome():
    chromosomeSatPasses = []
    for i in range(CHROMO_LENGTH):
        chromosomeSatPasses.append(genPasses())
    chromosome = Chromosome(chromosomeSatPasses)
    chromosome.fitness = fitness(chromosome)
    chromosome.satPassList = sorted(chromosome.satPassList, key=START_TIME_CMP)
    return chromosome


def nextPassChromosome(passes):
    """
    Take in next pass objects and output chromosomes
    """
    chromosomeSatPasses = []
    for item in passes:
        chromosomeSatPasses.append(item)
    chromosome = Chromosome(chromosomeSatPasses)
    chromosome.fitness = nextPassFitness(chromosome)
    chromosome.satPassList = sorted(chromosome.satPassList, key=RISE_TIME_CMP)
    return chromosome


def testChromosome(satPassList):
    chromosome = Chromosome(satPassList)
    chromosome.fitness = fitness(chromosome)
    chromosome.satPassList = sorted(chromosome.satPassList, key=START_TIME_CMP)
    return chromosome


def printPopulation(populateshit):
    for chromosome in populateshit:
        stringName = ""
        print("MORE CHROMOSOMES\n")
        print("FITNESS: " + str(nextPassFitness(chromosome)))
        for item in chromosome.satPassList:
            stringName += item.tle.name + " "
        print(chromosome.fitness, stringName)


def generatePopulation(chromosome):
    # chromo = generateChromosome()
    #chromosome = testChromosome(TEST_PASS_LIST)
    populationList = []

    # print("list without conflicts: \n")
    # for item in chromosome.satPassList:
    # print(item.name + " : %s" % str(item.startTime) + " : %s" % str(item.endTime))

    for i in range(POPULATION_SIZE):
        chromo = randomChromosome(chromosome)
        populationList.append(chromo)
        # print("list of conflicts: \n")
        # for item in chromo.satPassList:
        # print(item.name + " : %s" % str(item.startTime) + " : %s" % str(item.endTime))

    return populationList


def GA(population):
    """ Genetic algorithm for finding best suited order of sats """
    best = []  # Keep a list of the recent best solutions
    gen = 0
    while (1):
        gen += 1
        setFitness(population)  # check this
        population = sortByFitness(population)
        # this is for the case of variety fitness where largest is fittest:
        # others should be opposite
        best.append(population[-1])
        # since there is no definitive stopping value. i.e. if fitness was 0
        tournie(population)
        if (gen > 100):
            best = sortByFitness(best)
            print("best fitness: %s" % best[0].fitness)
            print("best order is:")
            for item in best[0].satPassList:
                print(item.tle.name)
            return best[0]

    print("generation: " + gen + "best: " + population[
        0].chromosomeString)  # TODO: chromosomeString should be Gene string.

'''

def getNeighbours(chromosome):



def HC(startChromosome):
    bestSoFar = startChromosome
    bestSoFar.fitness = setFitness(bestSoFar)
    while(bestSoFar.fitness is not 0):
        neighbours = getNeighbours(bestSoFar)
        neighbours = sortByFitness(neighbours)
        if(neighbours[0].fitness < bestSoFar.fitness):
            bestSoFar = neighbours[0]
        if(neighbours[0].fitness > bestSoFar.fitness):
            return bestSoFar
    return bestSoFar


def randomRestart(passes):
    startChromosome = nextPassChromosome(passes)
    gen = 0
    while(1):
        solution = HC(startChromosome)
        if(gen>100):
            return 
        startChromosome = nextPassChromosome(passes)

'''
