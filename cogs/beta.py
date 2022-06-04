import asyncio
import re
import discord

from helpers.bases import ConfirmView
from discord.ext import commands
from main import BerryBlush
from cogs.classes import embed_classes


    


class Beta(commands.Cog, command_attrs=dict(hidden=True)):
    """Unreleased and 'in-test' based commands; Hidden"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot
    
    

async def setup(bot):
    await bot.add_cog(Beta(bot))