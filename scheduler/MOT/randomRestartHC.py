from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
from ..services import Services
import sys


class MOTRandomRestartHC(MOT):

	def find(self,missionList,usefulTime):
			print(" Starting hillclimbing with random restart")

			nextPassListStart = _Helper.getNextPass(self,missionList)

			curOrder=list(nextPassListStart)
			i=0
			maxIterations = 50
			newScore=0
			oldScore=sys.maxsize
			bestNextPassList=[]
			#shuffle(curOrder)
			while i<maxIterations:
				shuffle(curOrder)									# find a different starting point
				hillclimbing = MOTRandomRestartHC._simpleRR(self,curOrder,usefulTime)		# find best order you can
				newScore,nextPassList = _Helper.fitnessFunction(self,hillclimbing,usefulTime)	# get the number from that order

				if(newScore<oldScore):
					oldScore=newScore
					curOrder=list(hillclimbing)
					bestOrder=list(curOrder)
					bestNextPassList=list(nextPassList)
				i+=1

			if i==maxIterations:
				print(" Random Restart HillClimbing finished with the order ")
				# for n in curOrder:
				# 	print(" {}".format(n.tle))
				#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
				print("And a score of {}".format(oldScore))
				return oldScore, bestNextPassList


	def _simpleRR(self,satList,usefulTime):
			""" In simple hill climbing, the first closer node is chosen"""
			bestNextPassList=[]
			print(" Starting simple hillclimbing for RR")
			maxIterations = 50
			maxNeighbours=200
			i=0
			oldScore = sys.maxsize
			newScore=0
			newOrder=[]
			curOrder=satList

			while i<maxIterations:
				listOfNearestNeighboursAndItself=[]
				generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)

				oldNeighbourScore=sys.maxsize
				for neighbour in generatorOfAllNeighboursIncItself:

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

				if (i%(maxIterations/10))==0:
					print(".")
					
			if i==maxIterations:
				print(" Simple HillClimbing for RR finished with the order ")
				# for n in curOrder:
				# 	pass
				# 	print(n)
				#print("{} curOrder could be global maxima with a score of {}".format(curOrder,oldScore))		
				print("And a score of {}".format(oldScore))
				return bestOrder
