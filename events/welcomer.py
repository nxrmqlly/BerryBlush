import discord

from discord.ext import commands, tasks
from main import BerryBlush

class Welcomer(commands.Cog):
    """Base class for welcome @member_join @member_remove events"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot

    

    @commands.Cog.listener('on_member_join')
    async def greet_welcome(self, member):
        print(f'{member} just joined!')
        chnl = self.bot.get_channel(929055855800901642)
        await chnl.send(f"Welcome **{member}** to the **{member.guild}**! Hope you have a great time here! :blueberries:")

    @commands.Cog.listener('on_member_remove')
    async def greet_goodbye(self, member):
        print(f'{member} just left!')
        chnl = self.bot.get_channel(929055855800901642)
        await chnl.send(f"**{member}** just left the server. They don't like blueberries :sob:")
    
    

async def setup(bot):
    await bot.add_cog(Welcomer(bot))