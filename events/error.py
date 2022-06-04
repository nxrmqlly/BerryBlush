import discord

from main import BerryBlush
from logging import Logger
from discord.ext import commands

class Error(commands.Cog):
    """Base class for error handling @command_error"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot
        self.logger: Logger = bot.logger

    @commands.Cog.listener()   
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.errors.CommandNotFound):
            return
        
        await ctx.send('```py\n'+str(error)+'\n```')
        self.logger.error(error)
        
        
            

async def setup(bot):
   await bot.add_cog(Error(bot))