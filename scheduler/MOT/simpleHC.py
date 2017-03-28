from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
import sys
import math

class MOTSimpleHC(MOT):

	def find(self,satList,usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""

		bestNextPassList=[]
		print(" Starting simple hillclimbing")
		maxIterations = 50
		# maxNeighbours=round((math.sqrt(len(satList))*5000))
		# #maxNeighbours=5000
		# print("maxneighbour{}".format(maxNeighbours))
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]
		maxN=0

		#Mission
		curOrder=satList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			#Generator/Iterator of all the neighbours
			print("Finding neighbours, this may take a while")
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			n=0
			#Find a smaller subset of all neighbours
			#for neighbour in generatorOfAllNeighboursIncItself:
				#if n==maxNeighbours:
				#	break
				#listOfNearestNeighboursAndItself.append(list(neighbour))
				#n+=1

			print("neighbours used {}".format(n))
			#Remove the current node from neighbour list
			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldNeighbourScore=sys.maxsize
			#Find the first better neighbour with a better score

			#print(listOfNearestNeighboursAndItself)
			newNeighbourScore=0
			for neighbour in generatorOfAllNeighboursIncItself:
				n+=1
				newNeighbourScore,nextPassList = _Helper.fitnessFunction(self, neighbour,usefulTime)

				#print(newNeighbourScore)
				#print(nextPassList)
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
				#print("happends")
				#print(nextPassList)
				bestNextPassList = list(nextPassList)
				#print("bestNextPassList")
				#print(bestNextPassList)
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

