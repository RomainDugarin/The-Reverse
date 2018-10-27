import discord

#
#   LIBRARY Channel FUNCTION
#
#
class channel():

    def findChannel(ctx, categoryName):
        try:
            for channel in ctx.message.server.channels:
                if channel.type == discord.ChannelType.category and categoryName.lower() == channel.name.lower():
                    return channel
            raise discord.client.NotFound
        except:
            return None


	