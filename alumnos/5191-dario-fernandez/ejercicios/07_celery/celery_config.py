from celery import Celery

BROKER_URL = 'redis://10.152.183.171'
BACKEND = 'redis://10.152.183.171:6379'
app = Celery('server', broker=BROKER_URL, backend=BACKEND, include=['calculator_operation'])
