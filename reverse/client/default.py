from discord.ext import commands

class DefaultCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pingo(self, ctx):
        print('Pong!')
        await ctx.send('Hello')

def setup(bot):
    bot.add_cog(DefaultCog(bot))