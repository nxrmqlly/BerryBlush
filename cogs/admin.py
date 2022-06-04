import discord
import os

from logging import Logger
from discord.ext import commands
from main import BerryBlush

class AdminOnly(commands.Cog, name="Admin", command_attrs=dict(hidden=True)):
    """Bot Admin/Owner reserved commands; Hidden"""
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx:commands.Context, extension):
        """Load a cog"""
        await self.bot.load_extension(f'cogs.{extension}')
        self.logger.info(f'Loaded Cog: {extension}.py')
        await ctx.send(f'Loaded {extension}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, extension):
        """Unload a cog"""
        if extension == 'admin':
            await ctx.send('Cannot unload admin.py')
            return

        await self.bot.unload_extension(f'cogs.{extension}')
        self.logger.info(f'Unloaded Cog: {extension}.py')
        await ctx.send(f'Unloaded {extension}')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, extension):
        """Reload a cog"""
        await self.bot.reload_extension(f'cogs.{extension}')
        self.logger.info(f'Reloaded Cog: {extension}.py')
        await ctx.send(f'Reloaded {extension}')

    @commands.command()
    @commands.is_owner()
    async def reloadall(self, ctx:commands.Context):
        """Reload all cogs and events"""
        self.logger.info('Reloading all cogs and events')
        for f in os.listdir('./cogs'):
            if f.endswith('.py'):
                await self.bot.reload_extension(f'cogs.{f[:-3]}')
                self.logger.info(f'Reloaded Cog: {f}')
        for f in os.listdir('./events'):
            if f.endswith('.py'):
                await self.bot.reload_extension(f'events.{f[:-3]}')
                self.logger.info(f'Reloaded Event: {f}')
        self.logger.info('Reloaded all cogs and events')
        await ctx.send('Reloaded all cogs and events')

    @commands.command()
    @commands.is_owner()
    async def reloadevents(self, ctx:commands.Context):
        """Reload all events"""
        self.logger.info('Reloading all events')
        for filename in os.listdir('./events'):
            if filename.endswith('.py'):
                try:
                    await self.bot.unload_extension(f'events.{filename[:-3]}')
                except:
                    pass
                try:
                    await self.bot.load_extension(f'events.{filename[:-3]}')
                except:
                    pass
        self.logger.info('Reloaded all events')
        await ctx.send('Reloaded all events')


    @commands.command(aliases=['clearconsole', 'clst', 'cls'])
    @commands.is_owner()
    async def clearterminal(self, ctx:commands.Context):
        """Clear the terminal window"""
        os.system('cls' if os.name == 'nt' else 'clear')
        await ctx.send('Terminal cleared')


   

    def __init__(self, bot: BerryBlush):
        self.bot = bot
        self.logger: Logger = bot.logger

async def setup(bot):
    await bot.add_cog(AdminOnly(bot))
