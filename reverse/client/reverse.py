import discord
from reverse.core._models import Server, Message

class Reverse():
	
	def __init__(self, **kwargs):
		self.client = Server(discord.Client())
		self.instance = self.getClient()

	def run(self, token: str):
		if(token is None):
			raise ValueError('Token can\t be empty.')
		if(not isinstance(token, str)):
			raise TypeError('Token is a string')
		self.token = token
		self.running = self.getClient().run(self.token)
		
	def getClient(self):
		return self.client.getInstance()

	async def on_ready(self):
		print('We have logged in as {0.user}'.format(self.getClient()))

	async def on_message(self, message):
		m = Message(message)
		print('We have detected a message from {0.author} saying {0.content}'.format(m.getData()))
