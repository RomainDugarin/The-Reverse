import asyncio, datetime

from reverse.core._models import Loop
from reverse.core import utils


class TaskService:

	__slots__ = [
		'name',
		'loop',
		'fields'
	]

	def __init__(self, name):
		self.name = name
		self.loop = asyncio.get_event_loop()
		self.fields = []

	def taskList(self):
		return self.fields

	def remove(self, loop):
		if(loop in self.fields):
			self.fields.pop(self.fields.index(loop))
		return self.fields

	def findTaskByName(self, name):
		for e in self.fields:
			if(name == e.getName()):
				return e
		return None

	def start(self, loop, *args, **kwargs):
		loop.start(*args, **kwargs)
		self.fields.append(loop)
		return loop

	def sleep_until(self, when, func):
		delta = utils.time_until(when)
		return self.createLoop(func, seconds=delta)
		
	def createLoop(self, func, *, seconds=0, minutes=0, hours=0, count=None, reconnect=True, loop=None, ctx=None, data=None):
		return Loop(func, seconds=seconds, minutes=minutes, hours=hours, count=count, reconnect=reconnect, loop=loop, ctx=ctx, data=data)
		# return tasks.Loop(func, seconds=seconds, minutes=minutes, hours=hours, count=count, reconnect=reconnect, loop=loop)
		
	def storeField(self, loop):
		self.fields.append(loop)
		return Loop

def loop(service, func, *, seconds=0, minutes=0, hours=0, count=None, reconnect=True, loop=None):
	return service.createLoop(func, seconds=seconds, minutes=minutes, hours=hours, count=count, reconnect=reconnect, loop=loop)
