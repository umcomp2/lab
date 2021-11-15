from celery import Celery

app = Celery('calculadora', broker='redis://localhost:6379', backend='redis://localhost:6379', include=['calculadora', ])