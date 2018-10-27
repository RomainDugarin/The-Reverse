
import requests, json
from .environment import environment
from .http import http
from .models import server

class reverseClient:

    def __init__(self):
        self.api = http()
        self.servers = []
        self.token = 'NTAxNzE5ODUxNzQwNTYxNDA4.DqeLLw.LYltOgK0Ho38SSa5HcwluXV7Xo8'
        self.creator = {
            'name': 'The Reverse Guy',
            'id': 124598335230312448,
            'game' : {
                'name': 'Creating himself.',
            },
            'version': 'V0.1',
            'description': 'Created by himself from the future.'
        }
        self.server = {
            'id' : {
                'privateConversation_id': None
            }
        }
        self.API_URL = 'http://localhost:9000/api/'

    async def registerServers(self, connectedServers):
        for cs in connectedServers:
            if cs.icon_url is None:
                print('none')
            value = server(cs.id, cs.name, cs.region, cs.icon, cs.large, cs.unavailable, cs.created_at, cs.member_count, cs.splash_url, cs.icon_url)
            await self.api.post('servers', json=value.__dict__())

    def registerMember(self, user):
        member = member(user.id, user.name, user.mention, user.created_at, user.avatar_url)
        return self.api.post('users', json=member)

    def getValidValue(value):
        typeValue = type(value)
        valid = [list]
        notValid = [discord.member.VoiceState]
        if typeValue in valid:
            return value[-1]
        elif typeValue in notValid:
            return None
        return value

    def findChannel(ctx, categoryName):
        try:
            for channel in ctx.message.server.channels:
                if channel.type == discord.ChannelType.category and categoryName.lower() == channel.name.lower():
                    return channel
            raise discord.client.NotFound
        except:
            return None