from celery import task

@task()
def pollForNew():
		print ( "Polling for new")
		try:
			mission_list = ms.findMissionsByStatus("New")
			for i in mission_list:
				i.status = ("Waiting")
				print("Count = %r" %i)
				pass
		except TLE.DoesNotExist as e:
			print("Already exists")	 


@task()
def pollQueue():
		count = 0
		while (count < 10):
			try:
				mission_list = ms.findMissionsByStatus("Ready")
				for i in mission_list:
					i.status = ("Tracked")
				print("Count = %r" %count)
				count+=1
				pass
			except TLE.DoesNotExist as e:
				print("Already exists")	 