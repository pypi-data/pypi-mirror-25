from celery.registry import tasks
from .job import Job, get_all_subclasses
from .signals import *

for cls in get_all_subclasses(Job):
    tasks.register(cls)