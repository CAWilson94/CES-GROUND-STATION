from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
from ..services import Services
import itertools
import sys

class MOTSteepestHC(MOT):

	def find(self,missionList, usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""
		bestNextPassList=[]
		print(" Starting steepest hillclimbing")
		maxIterations=25
		maxNeighbours=1500
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]
		
		nextPassListStart = _Helper.getNextPass(missionList)
		curOrder=list(nextPassListStart)

		
		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)

			oldNeighbourScore=sys.maxsize
			n=0
			for neighbour in generatorOfAllNeighboursIncItself:

				newNeighbourScore,nextPassList  = _Helper.fitnessFunction(self,neighbour,usefulTime)

				if(newNeighbourScore < oldNeighbourScore):
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore

				if n==maxNeighbours:
					break;

				n+=1
				
			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				bestNextPassList = list(nextPassList)
				i=0
			else:
				i+=1
			#print(newScore)

			if (i%(maxIterations/10))==0:
				print(".")
				
		if i==maxIterations:
			print(" Starting HillClimbing finished with the order ")
			# for n in curOrder:
			# 	pass
			# 	print(n)
			#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
			print("And a score of {}".format(oldScore))
			return oldScore,bestNextPassList

