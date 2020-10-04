from urllib.parse import quote as _uriquote
import sys
import json

import aiohttp
#from reverse import __version__


__version__ = '0.1.0'


async def json_or_text(response):
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['content-type'] == 'application/json':
            return json.loads(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text

class Route:
	BASE = 'https://api.betaseries.com'
	PARAMETERS = '?v=3.0'

	def __init__(self, method, path, fields='', **parameters):
		self.path = path
		self.method = method
		url = (self.BASE + self.path + self.PARAMETERS + fields)
		if parameters:
			self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
		else:
			self.url = url

class BetaSeries:

	def __init__(self, token, user_token):
		self.name = "BetaSeries"
		self.token = token
		self.bot_token = user_token
		self._session = aiohttp.ClientSession()

		user_agent = 'TheReverse (https://github.com/AlphaCodeCorp/The-Reverse {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
		self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

	def recreate(self):
		if(self._session.closed):
			self._session = aiohttp.ClientSession()

	async def request(self, route, *, files=None, **kwargs):
		method = route.method
		url = route.url

		headers = {
			'User-Agent': self.user_agent,
			'X-BetaSeries-Key': self.token,
			'Authorization': 'Bearer ' + self.bot_token,
			'Content-Type': 'application/json'
		}

		if('user' in kwargs):
			headers['Authorization'] = 'Bearer ' + kwargs['user']


		kwargs['headers'] = headers

		async with self._session.request(method, url, **kwargs) as r:

			data = await json_or_text(r)

			if(300 > r.status >= 200):
				return data
			
			if(r.status == 400):
				self.errors(data)

	def errors(self, data):
		code = data["errors"][0].get("code", 0)
		text = data["errors"][0].get("text", "...")
		raise ValueError("{}: {}".format(code, text))

	async def planning_member(self):
		r = Route('GET', '/planning/member')
		s = await self.request(r, user=self.bot_token)
		return r

		
