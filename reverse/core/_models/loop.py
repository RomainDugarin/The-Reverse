from discord.ext.tasks import Loop
from reverse.core._models import Context

class Loop(Loop):

	def __init__(self, func, *, seconds=0, minutes=0, hours=0, count=None, reconnect=True, loop=None, ctx: Context=None, data=None):
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
	
	def on_creation(self):
		print('Successfully created loop')

	def getData(self):
		pass
	
