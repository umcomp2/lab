from celery import Celery

app = Celery('task',broker = 'redis://localhost:6379', backend = 'redis://localhost:6379')
