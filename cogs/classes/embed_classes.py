import discord
import asyncio
import re

from helpers.bases import ConfirmView
from discord.ext import commands
from main import BerryBlush

class FieldDeleteSelection(discord.ui.View):
    ret_embed:discord.Embed
    def __init__(self, *,timeout: float = 60, embed: discord.Embed, bot: BerryBlush, ctx:commands.Context):
        super().__init__(timeout = timeout)
        self.embed = embed
        self.bot = bot
        self.ctx = ctx
        self.og_embed = embed
        
    @discord.ui.select(
        placeholder='Select an action.',
        options=[
            discord.SelectOption(label='Delete one by index', value='delete_one', emoji='🗑', description='Delete one field by index. (zero indexed)'),
            discord.SelectOption(label='Delete all', value='delete_all', emoji='🗑', description='Delete all fields.'),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        val = select.values[0]
        try:
            if val == 'delete_one':
                #make algorithm for deleting one field using a index
                await interaction.response.send_message('Please enter the index of the field you want to delete. (zero indexed)', ephemeral=True)
                def check(m):
                    return m.author == self.ctx.author and m.channel == self.ctx.channel
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await interaction.followup.send('Timed out.', ephemeral=True)
                    return

                try:
                    index = int(msg.content)
                except ValueError:
                    await interaction.followup.send('Please enter a valid index.', ephemeral=True)
                    await msg.delete()
                    return

                if index < 0 or index >= len(self.embed.fields):
                    await interaction.followup.send('Please enter a valid index. (zero indexed)', ephemeral=True)
                    await msg.delete()
                    return

                self.embed.remove_field(index)
                self.ret_embed = self.embed
                await msg.delete()
                await interaction.followup.send(f'Field deleted at index {index}.', ephemeral=True)
                self.stop()


            elif val == 'delete_all':
                self.ret_embed = self.embed.clear_fields()
                await interaction.response.send_message('Deleted all fields.', ephemeral=True)

                self.ret_embed = self.embed
                self.stop()
                
        except discord.HTTPException:
            self.ret_embed = self.og_embed
        
class EmbedMakerView(discord.ui.View):
    def __init__(self,*, init_msg:discord.Message, ctx:commands.Context, bot:BerryBlush):
        super().__init__(timeout=1200)
        self.embed: discord.Embed = discord.Embed(title='...', description='...')
        self.ctx: commands.Context = ctx
        self.bot = bot
        self.msg: discord.Message = init_msg
        self.selected: str
        self.check = lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel

    
    @discord.ui.select(
        placeholder='Select an component.',
        options=[discord.SelectOption(label=item, description=des, emoji=emoji, value=val, default=False) for item, des, emoji, val in [
            ('Title', 'The title of the embed', '✏', 'TITLE'),
            ('Description', 'The description of the embed', '📃', 'DESC'),
            ('URL', 'The URL of the embed', '🌐', 'URL'),
            ('Color', 'The embed accent color', '🎨', 'CLR'),
            ('Fields', 'Fields of the embed', '📚', 'FLDS'),
            ('Author', 'Author Name and Image of the embed', '🔺', 'AUTHR'),
            ('Footer', 'Footer Text and Image of the embed', '🔻', 'FOOTR'),
            ('Image', 'Image of the embed', '📷', 'IMG'),
            ('Thumbnail','Thumbnail (smaller image) of the embed', '📷', 'THMBNL')
            ]
        ],
        custom_id='embed:select',
        row=0
    )
    async def _select_clbk(self, interaction:discord.Interaction, select:discord.ui.Select):
        self.selected = select.values[0]
        for item in self.children:
            if item.custom_id in ('embed:button:add','embed:button:remove'):
                item.disabled=False


        for opt in select.options:
            opt.default = opt.value == self.selected


        await interaction.response.edit_message(content=f"Use the action buttons",view=self)

    #* adds or edits a embed component
    @discord.ui.button(
        label='Add',
        emoji='➕',
        style=discord.ButtonStyle.green,
        disabled=True,
        custom_id='embed:button:add'
    )
    async def add_btn_clbk(self, interaction:discord.Interaction, button:discord.ui.Button):
        #*The title
        if self.selected == 'TITLE':
            try:
                await interaction.response.send_message('Please respond with the Title for the embed.', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                self.embed.title = msg.content
                await interaction.followup.send(f'Updated Title to: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)

            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Title)', ephemeral=True)
            
        #* The description
        elif self.selected == 'DESC':
            try:
                await interaction.response.send_message('Please respond with the Description for the embed.', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                self.embed.description = msg.content
                await interaction.followup.send(f'Updated Description to: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)

            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Description)', ephemeral=True)

        #* The URL
        elif self.selected == 'URL':
            try:
                await interaction.response.send_message('Please respond with the URL for the embed.', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                if re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', msg.content):
                    self.embed.url = msg.content
                    await interaction.followup.send(f'Updated URL to: `{msg.content}`', ephemeral=True)
                else:
                    await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)

            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing URL)', ephemeral=True)

        #* The color
        elif self.selected == 'CLR':
            try:
                await interaction.response.send_message('Please respond with the Color for the embed. Supported:\n1) hex ➜ (`0x`, `0x#`, `#`)\n2) RGB ➜ `rgb(n, n, n)`', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                self.embed.color = discord.Color.from_str(msg.content)
                await interaction.followup.send(f'Updated Color to: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)
            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Color)', ephemeral=True)
            except ValueError:
                await interaction.followup.send(f'Invalid color (expecting hex or rgb)', ephemeral=True)
                
        #* The Author
        elif self.selected == 'AUTHR':
            try:
                await interaction.response.send_message('Please respond with the Author Name for the embed.', ephemeral=True)
                name: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                await name.delete()

                await interaction.followup.send('Please respond with the Author URL for the embed. (reply with `no`/`none` to add)', ephemeral=True)
                url: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                if not url.content.lower() in ('no','none'):
                    if not re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', url.content):
                        await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{url.content}`', ephemeral=True)
                        url_ = None
                    else:
                        url_ = url.content
                    await url.delete()
                else:
                    await url.delete()
                    url_ = None
                
                await interaction.followup.send('Please respond with the Author Icon URL for the embed. (reply with `no`/`none` to not add)', ephemeral=True)
                icon_url: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                # validating icon_url
                if not icon_url.content.lower() in ('no','none'):
                    if not re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', icon_url.content):
                        await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{icon_url.content}`', ephemeral=True)
                        icon_url_ = None
                    else:
                        icon_url_ = icon_url.content    

                    await icon_url.delete()
                else:
                    await icon_url.delete()

                    icon_url_ = None

                self.embed.set_author(name=name.content, url=url_, icon_url=icon_url_)
                
                await self.msg.edit(embed=self.embed)
            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Author)', ephemeral=True)

        #* The Footer
        elif self.selected == 'FOOTR':
            try:
                await interaction.response.send_message('Please respond with the Footer Text for the embed.', ephemeral=True)
                name: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                await name.delete()
                
                await interaction.followup.send('Please respond with the Footer Icon URL for the embed. (reply with `no`/`none` to not add)', ephemeral=True)
                icon_url: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                # validating icon_url
                if not icon_url.content.lower() in ('no','none'):
                    if not re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', icon_url.content):
                        await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{icon_url.content}`', ephemeral=True)
                        icon_url_ = None
                    else:
                        icon_url_ = icon_url.content    

                    await icon_url.delete()
                else:
                    await icon_url.delete()

                    icon_url_ = None

                self.embed.set_footer(text=name.content, icon_url=icon_url_)
                
                await self.msg.edit(embed=self.embed)
            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Author)', ephemeral=True)

        #* The fields
        elif self.selected == 'FLDS':
            try:
                await interaction.response.send_message('Please respond with the Field name to add to the embed.', ephemeral=True)
                name: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                await name.delete()
                await interaction.followup.send('Please respond with the Field value to add to the embed.', ephemeral=True)
                value: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                await value.delete()
                viewer = ConfirmView(timeout=40.0)
                await interaction.followup.send('Do you want this field to be inline?', ephemeral=True, view=viewer)
                await viewer.wait()
                inline = viewer.confirmed
                self.embed.add_field(name=name.content, value=value.content, inline=inline)

                await self.msg.edit(embed=self.embed)
            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Fields)', ephemeral=True)
        
        #* The image
        elif self.selected == 'IMG':
            try:
                await interaction.response.send_message('Please respond with the Image (url) for the embed.', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                if re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', msg.content):
                    self.embed.set_image(url=msg.content)
                    await interaction.followup.send(f'Updated Image (url) to: `{msg.content}`', ephemeral=True)
                else:
                    await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)

            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Image)', ephemeral=True)

        #* The thumbnail
        elif self.selected == 'THMBNL':
            try:
                await interaction.response.send_message('Please respond with the Thumbnail (url) for the embed.', ephemeral=True)
                msg: discord.Message = await self.bot.wait_for('message', timeout=60.0, check = self.check)
                if re.fullmatch(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#\?&//=]*)', msg.content):
                    self.embed.set_thumbnail(url=msg.content)
                    await interaction.followup.send(f'Updated Thumbnail (url) to: `{msg.content}`', ephemeral=True)
                else:
                    await interaction.followup.send(f'Invalid URL (include https/http protocols too.) Your input was: `{msg.content}`', ephemeral=True)
                await msg.delete()
                await self.msg.edit(embed=self.embed)

            except asyncio.TimeoutError:
                await interaction.followup.send(f'Timed out (editing Thumbnail)', ephemeral=True)
            
    @discord.ui.button(
        label='Remove',
        emoji='➖',
        style=discord.ButtonStyle.danger,
        disabled=True,
        custom_id='embed:button:remove'
    )
    async def rem_btn_clbk(self, interaction:discord.Interaction, button:discord.ui.Button):
        #* The title
        viewer_c = ConfirmView(timeout=40.0)
        await interaction.response.send_message('Are you sure you want to remove this Component?', ephemeral=True, view=viewer_c)
        await viewer_c.wait()
        if not viewer_c.confirmed:
            return await interaction.followup.send('Cancelled', ephemeral=True)
        
        try:
            if self.selected == 'TITLE':
                self.embed.title = None
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'DESC':
                self.embed.description = None
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'URL':
                self.embed.url = None
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'AUTHR':
                self.embed.set_author(name=None, url=None ,icon_url=None)
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'FOOTR':
                self.embed.set_footer(text=None, icon_url=None)
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'FLDS':
                viewer = FieldDeleteSelection(embed=self.embed, timeout=20.0, bot=self.bot, ctx=self.ctx)
                await interaction.followup.send('Please select the field you want to remove.', ephemeral=True, view=viewer)
                await viewer.wait()
                try:
                    await self.msg.edit(embed=viewer.ret_embed)
                except Exception:
                    pass
            elif self.selected == 'IMG':
                self.embed.set_image(url=None)
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'THMBNL':
                self.embed.set_thumbnail(url=None)
                await self.msg.edit(embed=self.embed)
            elif self.selected == 'CLR':
                self.embed.colour = None
                await self.msg.edit(embed=self.embed)

            await interaction.followup.send('Removed Component', ephemeral=True)
            
        except discord.HTTPException:
            return await interaction.response.send_message('Failed to remove the Component', ephemeral=True)

    @discord.ui.button(
        label='Send',
        emoji='📨',
        style=discord.ButtonStyle.primary,
        disabled=False,
        custom_id='embed:button:send'
    )
    async def snd_btn_clbk(self, interaction:discord.Interaction, button:discord.ui.Button):
        try:
            await interaction.response.send_message('Please respond with the channel to send this embed to. (supports channel mentions, and ids)', ephemeral=True)
            msg: discord.Message = await self.bot.wait_for('message', timeout=20.0, check=self.check)
            if re.fullmatch(r'(<#\d+>)|(\d+)', msg.content):
                try:
                    chnl = await self.bot.fetch_channel(int(msg.content\
                        .replace('<#', '')
                        .replace('>', '')
                    ))
                    await chnl.send(embed=self.embed)
                    await msg.delete()
                    await interaction.followup.send(f'Sent embed to {chnl.mention}', ephemeral=True)
                except discord.NotFound:
                    await interaction.followup.send('The channel was not found, try again!', ephemeral=True)
                except discord.Forbidden:
                    await interaction.followup.send('I am not allowed to fetch that channel!', ephemeral=True)
            else:
                await msg.delete()
                await interaction.followup.send('Invalid channel! (use mention or channel id)', ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.followup.send('Timed out (sending embed)', ephemeral=False)

        except:
            raise
    
    @discord.ui.button(
        emoji='🗑',
        style=discord.ButtonStyle.gray,
        disabled=False,
        custom_id='embed:button:delete'
    )
    async def del_btn_clbk(self, interaction:discord.Interaction, button:discord.ui.Button):
        viewer = ConfirmView(timeout=40.0)
        await interaction.response.send_message('Are you sure you want to delete this embed?', ephemeral=True, view=viewer)
        await viewer.wait()
        if viewer.confirmed:
            await self.msg.delete()
            await self.ctx.message.add_reaction('✅')
            await interaction.followup.send(content='Deleted embed.', ephemeral=True)
            self.stop()
        else:
            await interaction.followup.send('Cancelled deletion.', ephemeral=True)
    

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
                
            await self.msg.edit(content="**Timed out**", view=self)
            self.stop()
        except discord.NotFound:
            pass

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            return True
        else:
            await interaction.response.send_message(f'This isn\'t your interaction. (only `{self.ctx.author}` can use this)', ephemeral=True)
            return False
