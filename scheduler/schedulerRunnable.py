
class schedulerThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.couner = counter
	def run(self):
		print ("Starting " + self.name) 
		print("Polling for new now")
		try:
			Services.pollForNew()
		# ts.removeTLEById(180)

		except OperationalError:
			print("SchedulerThread - Could not find table (try makemigrations and migrate again)")
		print("Exiting "+ self.name)
	