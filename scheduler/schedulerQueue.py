class SchedulerQ():

	observers = []

	item = 0

	def registerObserver(observer):
		if(observer not in observers):
			observers.append(observers)

	def unregisterObserver(observer):
		if(observer in observers):
			observers.remove(observer)

	def notifyObservers():
		for o in observers:
			o.notify()

	def setItem(self, item):
		self.item = item

	def getItem(self):
		return self.item
