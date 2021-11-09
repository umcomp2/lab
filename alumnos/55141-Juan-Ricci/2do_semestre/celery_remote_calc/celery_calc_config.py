
from celery import Celery

app = Celery('celery_calc', broker='redis://analytics.juncotic.com:6379', backend='redis://analytics.juncotic.com:6379', include=['celery_calc'])

