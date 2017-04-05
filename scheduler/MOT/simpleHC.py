from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
import sys
import math

class MOTSimpleHC(MOT):

	def find(self,missionList,usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""

		bestNextPassList=[]
		print(" Starting simple hillclimbing")
		maxIterations = 50

		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[] 
		maxN=0

		#Mission
		curOrder=missionList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			#Generator/Iterator of all the neighbours
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			n=0

			oldNeighbourScore=sys.maxsize
			#Find the first better neighbour with a better score

			#print(listOfNearestNeighboursAndItself)
			newNeighbourScore=0
			for neighbour in generatorOfAllNeighboursIncItself:
				n+=1
				newNeighbourScore,nextPassList = _Helper.fitnessFunction(self, neighbour,usefulTime)

				if(newNeighbourScore < oldNeighbourScore):
					#Choose this better order
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					if(n>maxN):
						maxN=n
					break;
			
			#Is this better neighbour better than cur node
			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				bestNextPassList = list(nextPassList)
				i=0
			else:
				i+=1

			if (i%(maxIterations/10))==0:
				print(".")
				
		if i==maxIterations:
			print(" Simple HillClimbing finished with the order {}".format(bestNextPassList))
			print("And a score of {}".format(oldScore))
			print("neighbours used {}".format(maxN))

			return [oldScore,bestNextPassList]

