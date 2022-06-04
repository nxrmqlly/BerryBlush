"""
BerryBlush
~~~~~~~~~~~~~~~~~~~

A discord bot for the guild 'Blueberry Empire'

:copyright: (c) 2021-present Shadowed-codes (Nxrmqlly)
:license: MIT, see LICENSE for more details.
"""

__title__ = 'BerryBlush'
__author__ = 'Shadowed-codes (Nxrmqlly)'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-present Shadowed-codes (Nxrmqlly)'
__version__ = '1.0.0f'

import asyncio
import os, sys
import logging
import discord


from dotenv import load_dotenv
from discord.ext import commands, tasks


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
load_dotenv()


class BerryBlush(commands.AutoShardedBot):
    """The bot class, inherits from `commands.AutoShardedBot`"""
    logger: logging.Logger = logger
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or('b!', 'B!'),
            description='A bot for the server, "Blueberry Empire".',
            case_intensive=True,
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            activity=discord.Activity(type=discord.ActivityType.listening, name='lo-fi music | b!help'),
        )
        self.logger = logger
    @property
    def version(self):
        """The bot's current running version"""
        return __version__
        
    async def on_ready(self):
        print(f'<------------------------------->')
        print(f'Logged in as {self.user.name} with id {self.user.id}')
        print(f'Server Time: {self.launch_time.strftime("%Y/%m/%d %H:%M")}')
        print(f'discord.py Version: {discord.__version__}')
        print(f'Bot Version: {__version__}')
        print(f'Python Version: {sys.version}')
        print(f'<------------------------------->')

    async def setup_hook(self):  
        try:
            await self.load_extension('jishaku')
        except commands.errors.ExtensionAlreadyLoaded:
            pass
            
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                self.logger.info(f'Loaded Cog: {filename}')
                print(f"Loaded Cog: {filename}")
        cg_li = len([f for f in os.listdir("./cogs") if f.endswith(".py")])
        self.logger.info(f'Loaded {cg_li} cogs')
        print(f'=> Loaded {cg_li} cogs')

        for filename in os.listdir('./events'):
            if filename.endswith('.py'):
                await self.load_extension(f'events.{filename[:-3]}')
                self.logger.info(f'Loaded Event: {filename}')
                print(f"Loaded Event: {filename}")

        ev_li = len([f for f in os.listdir("./events") if f.endswith(".py")])
        self.logger.info(f'Loaded {ev_li} events')
        print(f'=> Loaded {ev_li} events')

    async def start(self):
        await self.login(os.getenv('TOKEN'))
        await self.connect(reconnect=True)


bot = BerryBlush()
bot.launch_time = discord.utils.utcnow()



async def start():
    await bot.start()

if __name__ == '__main__':
    asyncio.run(start())