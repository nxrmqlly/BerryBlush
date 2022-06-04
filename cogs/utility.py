import discord
import re
import asyncio

from discord.ext import commands
from main import BerryBlush
from cogs.classes import embed_classes
from helpers.bases import ConfirmView


class Utility(commands.Cog):
    """Utility/General use commands"""
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def suggest(self, ctx:commands.Context,*,txt:str =None):
        """Add a sugggestion"""
        if not txt:
            await ctx.reply(f"❌ Provide something to suggest!")
        chnl = self.bot.get_channel(927477354786353163)
        await chnl.send(embed=discord.Embed(title=f"Suggestion by {ctx.author}", description=f"`{txt}`"))


    @commands.command(aliases=['vote', 'review'])
    async def support(self, ctx:commands.Context):
        """Vote for/review the server"""
        em = discord.Embed(title = f"Vote and Review links for the server!", color = 0x2f3136)
        viewer = discord.ui.View()
        viewer.add_item(discord.ui.Button(label="Vote here!", url="https://top.gg/servers/928965734904770600", emoji="❤"))
        viewer.add_item(discord.ui.Button(label="Review here!", url="https://forms.gle/1yhwyEJUZAqs59wc9", emoji="❤"))

        await ctx.send(embed = em, view = viewer)

    @commands.command(aliases=['em', 'emb'])
    async def embed(self, ctx: commands.Context):
        """Interactive Embed maker"""
        init_em = discord.Embed(title='...', description='...')
        ms = await ctx.send('Loading..')
        await ms.edit(None, view=embed_classes.EmbedMakerView(init_msg=ms, ctx=ctx, bot=self.bot), embed=init_em)
        
async def setup(bot):
    await bot.add_cog(Utility(bot))