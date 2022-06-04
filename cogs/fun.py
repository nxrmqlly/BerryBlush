import discord
import random

from discord.ext import commands
from main import BerryBlush

class Fun(commands.Cog):
    """Commands that are purely made for fun. :P"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot

    @commands.command() #user is cool or no?
    async def cool(self, ctx:commands.Context,  member: discord.Member = None):
        """Determine a user's 'coolness' 😎"""
        if not member:
            member = ctx.author
        percent = random.randint(0,100)
        em = discord.Embed(title = f"{member.name} is {percent}% cool!", color = 0x7ac8ff)
        await ctx.reply(embed = em, mention_author=False)


    @commands.command(name = "8ball")
    async def _8ball(self, ctx:commands.Context, question: str = None):
        """Ask the magic 8ball a question"""
        response = [ 
            #yes
            "It is certain",
            "Without a doubt",
            "You may rely on it",
            "Yes definitely",
            "It is decidedly so",
            "As I see it, yes",
            "Most likely",
            "Yes",
            "Outlook good",
            "Signs point to yes",
            #neutral
            "Reply hazy, try again",
            "Better not tell you now",
            "Concentrate and ask again",
            #no
            "Don't count on it",
            "Outlook not so good",
            "My sources say No",
            "My reply is no",
            "Very doubtful"
        ]
        if question is None:
            return await ctx.reply("Please ask a question!", mention_author=False)
        else:
            await ctx.reply(f"🎱{random.choice(response)}", mention_author=False)

    
    @commands.command(aliases=['uwufy'])
    async def owofy(self, ctx:commands.Context,*, text:str):
        """Convert text into 'owo speak'"""
        if text.lower() == 'blueberry': #* Easter egg owo
            return await ctx.send('https://tenor.com/view/blueberry-racoon-bewwy-gif-20860794')
        b_o_f = random.choice([1,0])
        front,back='',''
        
        front = f"{random.choice(['UwU', 'HIII', '<3', 'OWO', 'H-'])} " if b_o_f else ''
        back = (f""" {random.choice(['fwendo', 'Huoh.', '._.',
                    '>_<', '>_>', ':P', ':3', ';3', 'x3', ':D', 
                    '(＾ｖ＾)', 'ㅇㅅㅇ', ''])}""") if not b_o_f else ''
        text = (
            front + text.lower()
                .replace('r', 'w')
                .replace('l', 'w')
                .replace('no', 'nu')
                .replace('have', 'has')
                .replace('you', 'u') + back)

        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(Fun(bot))