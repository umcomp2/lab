from celery import Celery
from postgresql_config import *

app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379", include = ['celery_admin'])
