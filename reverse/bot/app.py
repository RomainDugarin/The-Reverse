import discord


client = discord.Client(description="The Reverse", command_prefix="-", pm_help = False)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
