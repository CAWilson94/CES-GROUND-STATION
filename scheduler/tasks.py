from celery import shared_task


#app = Celery('tasks.py', broker='amqp://localhost')

@shared_task()
def pollForNew():
		print ( "Polling for new") 


@shared_task()
def pollQueue():
	print ( "Polling the queue")
