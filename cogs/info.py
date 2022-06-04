from cgitb import text
import discord
import helpers.constants as constants

from main import BerryBlush
from discord.ext import commands

class Info(commands.Cog):
    """Object information related commands"""
    def __init__(self, bot: BerryBlush):
        self.bot = bot

    @commands.command(aliases = ['ui', 'uinfo', 'whois'])
    async def userinfo(self, ctx:commands.Context, member: discord.Member = None):
        """Get info about a user."""
        f_usr = ''
        f_usr_acc_clr = ''
        init_msg = await ctx.send(embed=discord.Embed(color=0x2f3136).set_author(name=f"Loading", icon_url='https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif'))
        async with ctx.typing():
            if member is None:
                member = ctx.author
                f_usr = await self.bot.fetch_user(member.id)
                f_usr_acc_clr = str(f_usr.accent_color).upper()
            em = discord.Embed(color=0x2f3136)
            em.set_thumbnail(url = member.avatar.url if member.avatar else '    ')
            em.set_footer(text = f"User ID: {member.id}")
            em.set_author(name = f"{member.name}'s Information", icon_url = member.avatar.url if member.avatar else '   ')

            em.add_field(name = f"📄 User Information", value = f"""
                                                                ID: **{member.id}**
                                                                Nickname: **{member.nick if member.nick else ':x:'}**
                                                                Status: **{constants.MEMBER_STATUS[str(member.status)]}**
                                                                Is Bot: **{'✅' if member.bot else '❌'}**
                                                                Is Owner: **{'✅' if member == ctx.guild.owner else '❌'}**
                                                                Profile Color: {f_usr_acc_clr if not f_usr_acc_clr == 'NONE' else '❌'}
                                                                """, inline = True)

            em.add_field(name = f'📅 Created at', value = f"{discord.utils.format_dt(member.created_at, 'D')} ({discord.utils.format_dt(member.created_at, 'R')})", inline = False)
            em.add_field(name = f'📅 Joined at', value = f"{discord.utils.format_dt(member.joined_at, 'D')} ({discord.utils.format_dt(member.joined_at, 'R')})", inline = False)
            em.add_field(name = f'🥇 Badges', value = f'''{f"{constants.BKSLASH}".join([str(x).replace('UserFlags.', '').replace('_', ' ').title() for x in member.public_flags.all()]) or '**None**'}''')

            roles = [x.mention for x in member.roles if not x.is_default()]
            roles.reverse()
            if roles:
                em.add_field(name = f'👥 Roles', value=', '.join(roles) + f'\n\nTop Role: {member.top_role.mention} • Color: **{str(member.color).upper() if member.color is not discord.Color.default() else "Default"}**', inline=False)
            else:
                em.add_field(name = f'👥 Roles', value = ':x: No roles.', inline = False)


        await init_msg.delete()
        await ctx.send(embed=em)

    @commands.command(aliases = ['si', 'sinfo'])
    async def serverinfo(self, ctx:commands.Context):
        """Get info about the server."""
        init_msg = await ctx.send(embed=discord.Embed(color=0x2f3136).set_author(name=f"Loading", icon_url='https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif'))
        async with ctx.typing():
            guild = ctx.guild
            em = discord.Embed(color=0x2f3136)
            em.set_thumbnail(url = guild.icon.url)
            em.set_footer(text = f"Server ID: {guild.id}")
            em.set_author(name = f"{guild.name}'s Information", icon_url = guild.icon.url if guild.icon.url else '')

            enabled_features = []
            features = set(guild.features)

            for feature, label in constants.GUILD_FEATURES.items():
                if feature in features:
                    enabled_features.append(str(label))
            
            member_status = {
                'online': len([x for x in guild.members if x.status == discord.Status.online and not x.bot]),
                'dnd': len([x for x in guild.members if x.status == discord.Status.dnd and not x.bot]),
                'idle': len([x for x in guild.members if x.status == discord.Status.idle and not x.bot]),
            }            

            em.add_field(name = f"📄 Features", value=('\n'.join(enabled_features) if enabled_features else 'No features...'), inline=True)
            
            em.add_field(name = f'ℹ General Information', value = f"""
                                                                ID: **{guild.id}**
                                                                Owner: {guild.owner.mention}
                                                                File Size Limit: **{round(guild.filesize_limit / 1000000, 1)} MB**
                                                                Verification Level: **{str(guild.verification_level).replace('_', ' ').replace('none', 'no').title()}**
                                                                Roles: **{len(guild.roles)}**
                                                                """)

            em.add_field(name = "⌚ Created at", value = f"{discord.utils.format_dt(guild.created_at, 'D')} ({discord.utils.format_dt(guild.created_at, 'R')})", inline = False)
            em.add_field(name = "📷 Server content filter:", value=f"{constants.CONTENT_FILTER[guild.explicit_content_filter]}\n\u200b _ _", inline=False)

            em.add_field(name = "👥 Members", value = f"""
                Total: **{len(guild.members)}**
                Humans: **{len([x for x in guild.members if not x.bot])}**
                Bots: **{len([x for x in guild.members if x.bot])}**
                Limit: **{guild.max_members}**
                """)


            em.add_field(name = "👤 Member Statuses", value = f"""
                                                    Online: **{member_status['online']}**
                                                    Idle: **{member_status['idle']}**
                                                    DND: **{member_status['dnd']}**
                                                    """, inline = True)



            em.add_field(name = '🙂 Emojis', value = f"""
                                                    Static: **{len([x for x in guild.emojis if not x.animated])}/{guild.emoji_limit}**
                                                    Animated: **{len([x for x in guild.emojis if x.animated])}/{guild.emoji_limit}**
                                                    """, inline = True)

            em.add_field(name = "👻 AFK", value = f"""
                                                Channel: {guild.afk_channel.mention if guild.afk_channel else '*None*'}
                                                Timeout: **{guild.afk_timeout / 60} min** 
                                                """, inline = True)
            em.add_field(name = "📰 Channels", value = f"""
                                                    Text: **{len([x for x in guild.channels if x.type == discord.ChannelType.text])}**
                                                    Voice: **{len([x for x in guild.channels if x.type == discord.ChannelType.voice])}**
                                                    Categories: **{len([x for x in guild.channels if x.type == discord.ChannelType.category])}**
                                                    Rules Channel: {guild.rules_channel.mention if guild.rules_channel else '*None*'}   
                                                    """, inline = True)


        await init_msg.delete()
        await ctx.send(embed=em)
    
    @commands.command(aliases = ['ver'])
    async def version(self, ctx:commands.Context):
        """The bot's running version"""
        version = self.bot.version
        releaselvl = constants.RELEASE_LVL[''.join([x for x in list(version.replace('.', '')) if not x.isdigit()])]
        
        await ctx.send(
            embed = discord.Embed(
                title="BerryBlush release version",
                description=f'Version: *{self.bot.version}*\nRelease Level: *{releaselvl}*',
                color = 0x2f3136
            ) \
                .set_footer(text='Maintained by Nxrmqlly.')
                
        )
        
    @commands.command()
    async def uptime(self, ctx:commands.Context):
        """Uptime of the bot"""
        delta_uptime = discord.utils.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        em = discord.Embed(color=0x2f3136)
        em.set_author(name = f"My Uptime Info", icon_url = self.bot.user.avatar.url)
        em.add_field(name = f"⌚ Uptime", value = f"{days} day{'s' if not 1 == days else ''}, {hours} hour{'s' if not 1 == hours else ''}, {minutes} minute{'s' if not 1 == minutes else ''}, {seconds} second{'s' if not 1 == seconds else ''}.", inline = False)
        em.add_field(name = f"⌚ Launch Time", value = f"{discord.utils.format_dt(self.bot.launch_time, 'f')} ({discord.utils.format_dt(self.bot.launch_time, 'R')})", inline=False)
        em.set_footer(text = f"Time in UTC (GMT+0:00)")
        await ctx.send(embed = em)

async def setup(bot):
   await bot.add_cog(Info(bot))