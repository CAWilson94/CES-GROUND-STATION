from time import sleep
from threading import Thread

class SchedulerRunnable(Thread):

	def __init__(self, threadID, name, schedulerQ):
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.schedulerQ = schedulerQ

	def run(self):
		print ("Starting " + self.name) 
		counter = 0
		while(1):
			counter += 1
			if(counter > 100):
				counter = 0
			self.schedulerQ.setItem(counter)
			print("In Scheduler thread - " + str(counter))
			sleep(2)
		print("Exiting "+ self.name)



##############################################################
#
#	RotatorsRunnable(threadID, name, schedulerQ)
#		- threadID: and ID given to the thread
#		- name: the name for this thread
#		- schedulerQ: the queue to pull stellite passes from
#
##############################################################

class RotatorsRunnable(Thread):

	def __init__(self, threadID, name, schedulerQ):
		Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.schedulerQ = schedulerQ

	def run(self):
		print ("Starting " + self.name) 
		while(1):
			item = self.schedulerQ.getItem()
			print("In Rotators thread - " + str(item))
			sleep(2)
		print("Exiting "+ self.name)
	