from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
import sys

class MOTStochasticHC(MOT):

	def find(self,satList,usefulTime):
		""" does not examine any neighbors before deciding how to move. 
		Rather, it selects a neighbor at random, and moves to that one
		if it is better."""

		print(" Starting stochastic hillclimbing")
		maxIterations = 8000
		i=0
		oldScore = sys.maxsize  
		newOrder=[]
		bestNextPassList=[]
		curOrder=satList
		while i<maxIterations:
			
			#swap two random elements
			i1 = randint(0,len(curOrder)-1)
			i2 = randint(0,len(curOrder)-1)
			swap1 = curOrder[i1]
			swap2 = curOrder[i2]

			curOrder[i2]=swap1
			curOrder[i1]=swap2
			
			newScore,nextPassList = _Helper.fitnessFunction(self,curOrder,usefulTime)

			
			#Could make it so it only changes when it's a lot better or a little better
			if newScore < oldScore:
				#use that 
				oldScore=newScore
				bestOrder=list(curOrder)
				bestNextPassList=list(nextPassList)
				i=0
			else:
				i+=1
			
			if (i%(maxIterations/10))==0:
				print(".")

		if i==maxIterations:
			print(" Stochastic HillClimbing finished with the order ")
			print("And a score of {}".format(oldScore))
			return oldScore, bestNextPassList

