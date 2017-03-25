from scheduler.MOT.schedulerInterface import MOT
from scheduler.MOT._MOTHelper import _Helper
from datetime import date, datetime, timedelta
from random import shuffle,randint
import itertools
import sys

class MOTSimpleHC(MOT):

	def find(self,satList,usefulTime):
		""" In simple hill climbing, the first closer node is chosen"""

		#return _Helper.returnTwo()

		bestNextPassList=[]
		print(" Starting simple hillclimbing")
		maxIterations = 50
		i=0
		oldScore = sys.maxsize
		newScore=0
		newOrder=[]

		#Mission
		curOrder=satList

		while i<maxIterations:
			listOfNearestNeighboursAndItself=[]
			#Generator/Iterator of all the neighbours
			generatorOfAllNeighboursIncItself = itertools.permutations(curOrder)
			n=0
			maxNeighbours=500
			#Find a smaller subset of all neighbours
			for neighbour in generatorOfAllNeighboursIncItself:
				if n==maxNeighbours:
					break
				listOfNearestNeighboursAndItself.append(list(neighbour))
				n+=1

			#Remove the current node from neighbour list
			listOfNearestNeighbours = listOfNearestNeighboursAndItself[1:]

			oldNeighbourScore=sys.maxsize
			#Find the first better neighbour with a better score

			#print(listOfNearestNeighboursAndItself)
			newNeighbourScore=0
			for neighbour in listOfNearestNeighboursAndItself:
				#try:
				#print("neighbour")
				#print(neighbour)

				newNeighbourScore,nextPassList = _Helper.fitnessFunction(self, neighbour,usefulTime)
				#thing = _Helper.fitnessFunction(self, neighbour,usefulTime)
				
				#except TypeError as e:
					#print(e)
					#newNeighbourScore=0;
					#nextPassList=[]
					#newNeighbourScore=0
				# 	pass
				
				print(newNeighbourScore)
				#print(nextPassList)
				if(newNeighbourScore < oldNeighbourScore):
					#Choose this better order
					curOrder=neighbour
					oldNeighbourScore=newNeighbourScore
					newScore=newNeighbourScore
					break;

			# print("score")
			# print(newNeighbourScore)
			# print(nextPassList)
			
			#Is this better neighbour better than cur node
			#print("newScore")
			#print(newScore)#
			if newScore < oldScore:
				oldScore=newScore
				bestOrder = list(curOrder)
				print("happends")
				print(nextPassList)
				bestNextPassList = list(nextPassList)
				print("bestNextPassList")
				print(bestNextPassList)
				i=0
			else:
				i+=1

			# if ((i%maxIterations)/10)=maxIterations:
			# 	print(".")
				
		if i==maxIterations:
			print(" Simple HillClimbing finished with the order {}".format(bestNextPassList))
			print("And a score of {}".format(oldScore))
			return [oldScore,bestNextPassList]

