from discord.ext import commands
from reverse.core._models import Server, Message, Context


class Reverse():
	
	def __init__(self, command_prefix, description=None, **kwargs):
		kwargs=kwargs['kwargs']
		print('Reverse : {}'.format(kwargs))
		self.client = Server(commands.Bot(command_prefix=command_prefix, description=description, kwargs=kwargs))
		self.instance = self.getClient()
		self.cogs = []
		self.linkCogs(['reverse.client.default'])

	def run(self, token: str):
		if(token is None):
			raise ValueError('Token can\t be empty.')
		if(not isinstance(token, str)):
			raise TypeError('Token is a string')
		self.token = token
		self.running = self.getClient().run(self.token)
		
	def getClient(self) -> commands.Bot:
		return self.client.getInstance()

	def linkCogs(self, cogs: list):
		if(cogs is not None):
			self.cogs.extend(cogs)
		for cog in self.cogs:
			try:
				self.getClient().load_extension(cog)
				print('Load {}'.format(cog))
			except Exception as e:
				print('{} cannot be loaded. [{}]'.format(cogs, e))
				self.getLogger()

	def getLogger(self):
		pass

	def getCommands(self) -> commands:
		return commands

	def createCommand(self, func, **kwargs) -> commands.Command:
		return commands.Command(func=func, kwargs=kwargs)

	def addCommand(self, func, **kwargs) -> commands.command:
		command = commands.Command(func=func, kwargs=kwargs)
		self.getClient().add_command(command)
		return command

	async def on_ready(self):
		print('We have logged in as {0.user}'.format(self.getClient()))

	async def on_message(self, message):
		m = Message(message)
		print('We have detected a message from {0.author} saying {0.content}'.format(m.getData()))
		await self.getClient().process_commands(message)