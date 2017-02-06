from Chromosome import Chromosome

class Population(object):
	def RandPopulation(self,popSize):
		if ((popSize % 2) != 0):
			popSize += 1;
		population = []
		for i in range (popSize):
			c = Chromosome()
			population.append(c.randomChromo(()))
		return population
		
Population().RandPopulation(4)