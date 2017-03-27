from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
import sys

class MOTSteepestHC(MOT):

	def find(self,satList, usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""
		bestNextPassList=[]
		print(" Starting steepest hillclimbing")
		maxIterations = 50
		maxNeighbours=5000
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]
		curOrder=satList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			n=0
			for neighbour in generatorOfAllNeighboursIncItself:
				if n==maxNeighbours:
					break
				listOfNearestNeighboursAndItself.append(list(neighbour))
				n+=1

			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldNeighbourScore=sys.maxsize
			for neighbour in listOfNearestNeighbours:

				newNeighbourScore,nextPassList  = _Helper.fitnessFunction(self,neighbour,usefulTime)

				if(newNeighbourScore < oldNeighbourScore):
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					break;

			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				bestNextPassList = list(nextPassList)
				i=0
			else:
				i+=1
			#print(newScore)

			if i%maxIterations/10:
				print(".")
				
		if i==maxIterations:
			print(" Simple HillClimbing finished with the order ")
			# for n in curOrder:
			# 	pass
			# 	print(n)
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return oldScore,bestNextPassList

