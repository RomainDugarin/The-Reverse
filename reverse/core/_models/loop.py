from discord.ext.tasks import Loop
from reverse.core._models import Context

class Loop(Loop):

	def __init__(self, func, *, seconds=0, minutes=0, hours=0, count=None, reconnect=True, loop=None, ctx: Context=None, data: dict=None):
		super().__init__(
			func,
			seconds=seconds,
			minutes=minutes,
			hours=hours,
			count=count,
			reconnect=reconnect,
			loop=loop
		)
		self.ctx = ctx
		self.data = data
		self.run()
	
	def run(self):
		self.on_creation()

	def getName(self):
		return self.coro.__name__

	def getContext(self):
		return self.ctx

	def getData(self):
		return self.data

	def isRunning(self):
		return self.is_running()

	def change_interval(self, *, seconds=0, minutes=0, hours=0):
		super().change_interval(seconds=seconds, minutes=minutes, hours=hours)

	def restart(self, **kwargs):
		_old = {
			"ctx": self.ctx,
			"data": self.data
		}
		_interval = {
			"seconds": float(kwargs.get("seconds", 0)),
			"minutes": float(kwargs.get("minutes", 0)),
			"hours": float(kwargs.get("hours", 0))
		}
		if(not all(value == 0 for value in _interval.values())):
			self.change_interval(**_interval)

		super().restart(**_old)

	def stop(self):
		super().stop()
		
	def on_creation(self):
		print('Successfully created loop')

	def getData(self):
		pass
	
