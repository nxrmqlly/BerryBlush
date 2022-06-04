import discord
import re
import asyncio

from discord.ext import commands
from main import BerryBlush

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

    @commands.command(aliases=['em']) #! DEPRECATED
    async def embed(self, ctx:commands.Context):
        """! deprecated do not use"""
        return await ctx.send("Sorry, the `embed` command has been archived.")
        em = discord.Embed(title = f"...", description = '...', color = 0x000000)
        await ctx.send("The BerryBlush custom embed maker!\nRespond to following messages to edit your embed!\n\nStarting in 5 seconds...")
        await asyncio.sleep(5)

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel


        # TITLE
        await ctx.send(embed = em, content = "Please respond with the **Title** for the embed. You have 1 minute")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")
        
        em.title = x.content


        # DESCRIPTION
        await ctx.send(embed = em, content = "Please respond with the **Description** for the embed. You have 1 minute")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

        em.description = x.content


        # FIELDS
        await ctx.send(embed = em, content = "Please respond with the **Fields** for the embed (respond with `no` to skip). You have 5 minutes\nDo it this way: `name | value | *True/False = False`\n(name | value | inline) (`\" | \"` is a separator)\nAdd more fields by Creating a `newline`")
        try:
            x = await self.bot.wait_for('message', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

        if x.content == "no":
            pass

        else:

            fields = x.content.split("\n")
            for field in fields:
                if field:
                    if not field.split(' |')[2]:
                        name, value = field.split(" |")
                        inline = True

                    else:
                        name, value, inline = field.split(" |")
                        inline = True if inline.title() == "True" else False


                    em.add_field(name=name, value=value, inline=inline)

        # AUTHOR
        await ctx.send(embed = em, content = "Please respond with the **Author** for the embed (respond with `no` to skip). You have 1 minute\nDo it this way: `name | [url]`")

        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")
        
        if x.content == "no":
            pass
        else:
            if not ' |' in x.content:
                author = x.content
                em.set_author(name=author)

            else:
                author, url = x.content.split(" |")

                if re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url):
                    em.set_author(name=author, icon_url=url)
            

        # FOOTER 
        await ctx.send(embed = em, content = "Please respond with the **Footer** for the embed (respond with `no` to skip). You have 1 minute\nDo it this way: `name | [url]`")

        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

        if x.content == "no":
            pass
        else:
            if not ' |' in x.content:
                footer = x.content
                em.set_footer(name=footer)
            else:
                footer, url = x.content.split(" |")
                if re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url):
                    em.set_footer(text=footer, icon_url=url)

        # IMAGE
        await ctx.send(embed = em, content = "Please respond with the **Image** for the embed (respond with `no` to skip). You have 1 minute (must be a valid url)")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")
        
        if x.content == "no":
            pass
        else:
            if re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', x.content):
                em.set_image(url=x.content)

        # THUMBNAIL
        await ctx.send(embed = em, content = "Please respond with the **Thumbnail** for the embed (respond with `no` to skip). You have 1 minute. (must be a valid url).")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")
        
        if x.content == "no":
            pass
        else:
            if re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', x.content):
                em.set_thumbnail(url=x.content)


        # COLOUR
        await ctx.send(embed = em, content = "Please respond with the **Colour** for the embed (respond with `no` to skip). You have 1 minute")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

        if x.content == "no":
            pass

        else:
            if x.content.startswith("#"):
                em.colour = int(x.content[1:], 16)
            else:
                em.colour = int(x.content, 16)

        #CHANNEL TO POST IN
        await ctx.send(embed = em, content = "Please respond with the **Channel** to post this embed. You have 1 minute")
        try:
            x = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

        if isinstance(x.content, discord.TextChannel):
            await x.conent.send(embed=em)

        await ctx.send(embed = em)

   
async def setup(bot):
    await bot.add_cog(Utility(bot))