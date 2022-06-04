import discord

from discord.ext import commands, tasks
from main import BerryBlush

class StatDocks(commands.Cog):
    def __init__(self, bot: BerryBlush):
        self.bot = bot

    async def cog_load(self) -> None:
        self.membercount_.start()
        self.utctime_.start()

    @tasks.loop(minutes=6)
    async def membercount_(self):
        if not self.bot.is_ready():
            return
        guild = self.bot.get_guild(928965734904770600)
        human_members = len([x for x in guild.members if not x.bot])
        chnl: discord.VoiceChannel = self.bot.get_channel(929058994096603256)
        await chnl.edit(name=f'Members: {human_members}') 

    @tasks.loop(minutes=3)
    async def utctime_(self):
        if not self.bot.is_ready():
            return
        chnl: discord.VoiceChannel = self.bot.get_channel(982588719871705139)
        await chnl.edit(name=f'{discord.utils.utcnow().strftime("%Y/%m/%d %H:%M")}')

async def setup(bot):
    await bot.add_cog(StatDocks(bot))