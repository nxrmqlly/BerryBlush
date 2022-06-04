import discord

from discord.ext import commands
from main import BerryBlush

class Moderation(commands.Cog):
    """Moderator/Admin only commands"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx:commands.Context, member: discord.Member, reason:str='No reason provided'):
        """Kick a member from the guild"""
        await ctx.guild.kick(member)
        await ctx.reply(f'✅ **{member}** has been kicked.\nReason: **{reason}**\nModerator: **{ctx.message.author}**',mention_author=False)

    @commands.command(aliases = ["purge"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx:commands.Context, amount: int = 0):
        """Purge messages in a channel"""
        if amount == 0:
            await ctx.reply(":x: Please Provide a number of messages to Purge!", mention_author=False)
        else:
            await ctx.channel.purge(limit = amount + 1)


    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx:commands.Context, member: discord.Member, reason:str='No reason provided'):
        """Ban a user from the guild"""
        await ctx.guild.ban(member,reason=reason)
        await ctx.reply(f'✅ **{member}** has been banned.\nReason: **{reason}**\nModerator: **{ctx.message.author}**',mention_author=False)


    @commands.command(aliases = ["sm", "delay"])
    @commands.has_permissions(manage_channels = True)
    async def slowmode(self, ctx:commands.Context, seconds: int = 0):
        """Quickly change slowmode of the channel"""
        if seconds == 0:
            await ctx.reply("✅ Turned off slowmode", mention_author=False)
            await ctx.channel.edit(slowmode_delay = 0)
        elif seconds > 21600:
            await ctx.reply("❌ Cannot set the slowmode Above 6 hours!", mention_author=False)
        else:
            await ctx.channel.edit(slowmode_delay = seconds)
            await ctx.reply(f"✅ Slowmode set to {seconds} Seconds.", mention_author=False)

    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members = True)
    async def unban(self,ctx, *,member = None):
        """Unban a member, if found, from the guild"""
        if not member:
            await ctx.reply("❌ Provide a user to unban! Format: `Username#1234`", mention_author=False)
            return

        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return await ctx.reply(f'✅ Unbanned **{user.name}**\nModerator: **{ctx.message.author}**', mention_author=False)
            
        await ctx.reply("❌ Couldn't Unban because the user was not found in previously banned entries", mention_author=False)


    @commands.command(aliases = ['nickname'])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx:commands.Context, member: discord.Member = None, *,nick: str = None):
        """Quickly change a member's nickname"""
        nickname = ''
        if not member:
            return await ctx.reply(f':x: Incorrect usage!\n`b!nick <member> [nickname]`', mention_author=False)
        if not nick:
            nickname = member.name
            await member.edit(nick=nickname)
            await ctx.reply(f'✅ Reset nickname for **{member}**', mention_author=False)
            return

        await member.edit(nick=nick)
        await ctx.reply(f"✅ Changed **{member}**'s nickname to **{nick}**", mention_author=False)


async def setup(bot):
    await bot.add_cog(Moderation(bot))