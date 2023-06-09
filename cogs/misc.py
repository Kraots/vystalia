import re
import math
import pytz
import time
import random
import psutil
import wikipedia
import simpleeval
import matplotlib.pyplot as plt
from datetime import datetime

import disnake
from disnake.ext import commands

from dulwich.repo import Repo

from serpapi import GoogleSearch

import utils
from utils import (
    Context,
    Rules,
    AFK,
    Mutes,
    RoboPages,
    FieldPageSource,
    Birthday
)

from jishaku.shell import ShellReader

from main import Vystalia

SERVER_AD = """
𓆱𓇟.ꜱᴀʏ ʜᴇʟʟᴏ ᴛᴏ ᴀꜱᴛᴇᴍɪᴀ.𓇟𓆱
-----------------------------------
ᴅᴏ ʏᴏᴜ ʜᴀᴘᴘᴇɴ ᴛᴏ ʙᴇ ʟᴏꜱᴛ?, ᴀʀᴇ ʏᴏᴜ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ ꜱᴏᴍᴇᴛʜɪɴɢ ɴᴇᴡ ᴀɴᴅ ɪɴᴛᴇʀᴇꜱᴛɪɴɢ? ᴡᴇʟʟ ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴛʜɪꜱ ꜱᴇʀᴠᴇʀ<3 

ᴡᴇ ʜᴀᴠᴇ: 

❁•ꜰʀɪᴇɴᴅʟʏ ᴏᴡɴᴇʀꜱ, ᴀᴅᴍɪɴꜱ ᴀɴᴅ ᴍᴏᴅꜱ 
❁•ᴀ ᴜɴɪqᴜᴇ ᴀɴᴅ ᴄᴜꜱᴛᴏᴍ ʙᴏᴛ
❁•ᴄᴏᴏʟ ʀᴏʟᴇꜱ ᴀɴᴅ ᴏʀɢᴀɴɪᴢᴇᴅ ɪɴᴛʀᴏᴅᴜᴄᴛɪᴏɴꜱ
❁•ᴀᴍᴀᴢɪɴɢ ᴘᴇᴏᴘʟᴇ ᴀɴᴅ ꜰʀɪᴇɴᴅꜱ
❁•ᴀ ꜰᴜɴ ᴇxᴄɪᴛɪɴɢ ꜱᴇʀᴠᴇʀ
❁•ᴇᴍᴏᴊɪꜱ ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ
❁•ᴀɴᴅ ᴀɴ ᴀᴄᴄᴇᴘᴛɪɴɢ ᴀɴᴅ ʟᴏᴠɪɴɢ ᴄᴏᴍᴍᴜɴɪᴛʏ, ᴡʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ꜰᴇᴇʟ ᴄᴏᴍꜰᴏʀᴛᴀʙʟᴇ ᴀɴᴅ ʙᴇ ʏᴏᴜʀꜱᴇʟꜰ


꧁•❁ ʟɪɴᴋ: https://discord.gg/ewZ7hQbJhj ꧂
"""

functions = {
    'sqrt': lambda x: math.sqrt(x),
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tan': lambda x: math.tan(x),
    'ceil': lambda x: math.ceil(x),
    'floor': lambda x: math.floor(x),
    'sinh': lambda x: math.sinh(x),
    'cosh': lambda x: math.cosh(x),
    'tanh': lambda x: math.tanh(x),
    'abs': lambda x: math.fabs(x),
    'log': lambda x: math.log(x)
}


class Misc(commands.Cog):
    """Miscellaneous commands, basically commands that i have no fucking idea where to fucking put so they just come in this category."""
    def __init__(self, bot: Vystalia):
        self.bot = bot
        self.github_client = utils.GithubClient(bot)

    @property
    def display_emoji(self) -> str:
        return '🔧'

    @commands.command()
    async def ping(self, ctx: Context):
        """See the bot's ping.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        ping = disnake.Embed(title="Pong!", description="_Pinging..._", color=utils.blurple)
        start = time.time() * 1000
        msg = await ctx.better_reply(embed=ping)
        end = time.time() * 1000
        ping = disnake.Embed(
            title="Pong!",
            description=f"Websocket Latency: `{(round(self.bot.latency * 1000, 2))}ms`"
            f"\nBot Latency: `{int(round(end-start, 0))}ms`"
            f"\nResponse Time: `{(msg.created_at - ctx.message.created_at).total_seconds()/1000}` ms",
            color=utils.blurple
        )
        ping.set_footer(text=f"Online for {utils.human_timedelta(dt=self.bot.uptime, suffix=False)}")
        await msg.edit(embed=ping)

    @commands.command()
    async def uptime(self, ctx: Context):
        """See how long the bot has been online for.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        uptime = disnake.Embed(
            description=f"Bot has been online since {utils.format_dt(self.bot.uptime, 'F')} "
                        f"(`{utils.human_timedelta(dt=self.bot.uptime, suffix=False)}`)",
            color=utils.blurple
        )
        uptime.set_footer(text=f'Bot made by: {self.bot._owner}')
        await ctx.better_reply(embed=uptime)

    @commands.command(name='metrics')
    async def show_metrics(self, ctx: Context):
        """Shows the metrics as well as some info about the bot."""

        em = disnake.Embed(title='Metrics', description='_Fetching Metrics..._', colour=utils.invisible)
        start = time.time() * 1000
        msg = await ctx.better_reply(embed=em)
        end = time.time() * 1000

        process = psutil.Process()
        mem = process.memory_full_info()
        cpu_usage = psutil.cpu_percent()
        physical = utils.natural_size(mem.rss)
        threads = process.num_threads()
        pid = process.pid

        commands = 0
        for cmd in self.bot.walk_commands():
            commands += 1

        extensions = len(self.bot.extensions)

        em = disnake.Embed(title='Metrics', colour=utils.invisible)
        em.add_field(
            name='Ping',
            value=f'Websocket Latency: `{(round(self.bot.latency * 1000, 2))}ms`'
                  f'\nBot Latency: `{int(round(end-start, 0))}ms`'
                  f'\nResponse Time: `{(msg.created_at - ctx.message.created_at).total_seconds()/1000}` ms',
            inline=False
        )
        em.add_field(
            name='Memory Usage',
            value=f'CPU: {cpu_usage}%'
                  f'\nRAM Usage: {physical}'
                  f'\nThreads: {threads}'
                  f'\nPID: {pid}',
            inline=False
        )
        em.add_field(
            name='Extras',
            value=f'Running on commit [``{self.bot.git_hash[:7]}``](https://github.com/Kraots/vystalia/tree/{self.bot.git_hash})'
                  f'\nCommands: {commands}'
                  f'\nExtensions: {extensions}'
                  f'\nUptime: {utils.human_timedelta(dt=self.bot.uptime, suffix=False)}',
            inline=False
        )

        em.set_footer(
            text=f'Bot made by: {self.bot._owner}',
            icon_url=self.bot.user.display_avatar.url
        )

        await msg.edit(embed=em)

    @commands.command(name='invite', aliases=('inv',))
    async def _invite(self, ctx: Context):
        """Sends an invite that never expires.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        await ctx.better_reply('https://discord.gg/khPXDbDMT9')

    @commands.command(aliases=('ad',))
    async def serverad(self, ctx: Context):
        """See the server's ad.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        ad = disnake.Embed(color=utils.blurple, title='Here\'s the ad to the server:', description=SERVER_AD)
        ad.set_footer(text=f'Requested by: {utils.format_name(ctx.author)}')

        await ctx.better_reply(embed=ad)

    @commands.group(
        name='rules', invoke_without_command=True, case_insensitive=True, aliases=('rule',)
    )
    async def server_rules(self, ctx: Context, rule: int = None):
        """Sends the server's rules. If ``rule`` is given, it will only send that rule.

        `rule` **->** The number of the rule you wish to see.
        """

        rules: Rules = await self.bot.db.get('rules')
        if rules is None:
            return await ctx.reply(f'{ctx.denial} There are currently no rules set. Please contact an admin about this!')
        embeds = []

        if rule is None:
            em = disnake.Embed(title='Rules', color=utils.blurple)
            em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')
            for index, rule in enumerate(rules.rules):
                if index in (10, 20, 30, 40, 50):  # Show 10 rules per embed
                    embeds.append(em)
                    em = disnake.Embed(title='Rules', color=utils.blurple)
                    em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')

                if em.description is None:
                    em.description = f'`{index + 1}.` {rule}'
                else:
                    em.description += f'\n\n`{index + 1}.` {rule}'
            embeds.append(em)

        else:
            em = disnake.Embed(title='Rules', color=utils.blurple)
            if rule <= 0:
                return await ctx.reply(f'{ctx.denial} Rule cannot be equal or less than `0`')
            try:
                _rule = rules.rules[rule - 1]
                em.description = f'`{rule}.` {_rule}'
            except IndexError:
                return await ctx.reply(f'{ctx.denial} Rule does not exist!')
            em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')
            embeds.append(em)

        await ctx.better_reply(embeds=embeds)

    @server_rules.command(name='add')
    @utils.is_admin()
    async def server_rules_add(self, ctx: Context, *, rule: str):
        """Adds a rule to the server's rules.

        `rule` **->** The rule to add.
        """

        rules: Rules = await self.bot.db.get('rules')
        if rules is None:
            await self.bot.db.add('rules', Rules(
                id=self.bot._owner_id,
                rules=[rule]
            ))
        else:
            rules.rules += [rule]
            await rules.commit()

        await ctx.reply(f'> 👌 📝 `{rule}` successfully **added** to the rules.')

    @server_rules.command(name='edit')
    @utils.is_admin()
    async def server_rules_edit(self, ctx: Context, rule: int, *, new_rule: str):
        """Edits an existing rule.

        `rule` **->** The number of the rule to edit.
        `new_rule` **->** The new rule to replace it with.
        """

        rules: Rules = await self.bot.db.get('rules')
        if rules is None:
            return await ctx.reply(f'{ctx.denial} There are currently no rules set.')
        elif rule == 0:
            return await ctx.reply('Rule cannot be ``0``')

        rule -= 1
        try:
            rules.rules[rule] = new_rule
        except IndexError:
            return await ctx.reply('Rule does not exist!')
        await rules.commit()

        await ctx.reply(f'> 👌 📝 Successfully **edited** rule `{rule + 1}` to `{new_rule}`.')

    @server_rules.command(name='remove', aliases=('delete',))
    @utils.is_admin()
    async def server_rules_remove(self, ctx: Context, rule: int):
        """Removes a rule from the server's rules by its number.

        `rule` **->** The number of the rule to remove.
        """

        rules: Rules = await self.bot.db.get('rules')
        if rules is None:
            return await ctx.reply(f'{ctx.denial} There are currently no rules set.')
        else:
            if rule <= 0:
                return await ctx.reply(f'{ctx.denial} Rule cannot be equal or less than `0`')
            try:
                rules.rules.pop(rule - 1)
            except IndexError:
                return await ctx.reply(f'{ctx.denial} Rule does not exist!')
            await rules.commit()

        await ctx.reply(f'> 👌 Successfully **removed** rule `{rule}`.')

    @server_rules.command(name='clear')
    @utils.is_owner()
    async def server_rules_clear(self, ctx: Context):
        """Deletes all the rules."""

        rules: Rules = await self.bot.db.get('rules')
        if rules is None:
            return await ctx.reply(f'{ctx.denial} There are currently no rules set.')
        else:
            await self.bot.db.delete('rules', {'_id': rules.pk})

        await ctx.reply('> 👌 Successfully **cleared** the rules.')

    @commands.group(
        name='nick', invoke_without_command=True, case_insensitive=True, aliases=('nickname',)
    )
    async def change_nick(self, ctx: Context, *, new_nickname: str):
        """Change your nickname to your desired one.

        `new_nickname` **->** The new nickname you wish to change to.
        """

        if utils.check_string(new_nickname) or utils.check_profanity(new_nickname, bad_words=self.bot.bad_words.keys()):
            return await ctx.reply(
                f'{ctx.denial} Cannot change your nickname because the nickname you chose '
                'has too less pingable characters, is a bad word or is too short (minimum is **4**).'
            )
        elif len(new_nickname) > 32:
            return await ctx.reply('Nickname has too many characters! (maximum is **32**)')

        await ctx.author.edit(nick=new_nickname)
        await ctx.reply(f'I have changed your nickname to `{new_nickname}`')

    @change_nick.command(name='reset', aliases=('remove',))
    async def remove_nick(self, ctx: Context):
        """Removes your nickname."""

        if utils.check_string(ctx.author.name) or utils.check_profanity(ctx.author.name, bad_words=self.bot.bad_words.keys()):
            return await ctx.reply(
                f'{ctx.denial} Cannot remove your nickname because your username '
                'has too less pingable characters, is a bad word or is too short (minimum is **4**).'
            )
        await ctx.author.edit(nick=None)
        await ctx.reply('I have removed your nickname.')

    @commands.command(name='avatar', aliases=('av',))
    async def _av(self, ctx: Context, *, member: disnake.Member = None):
        """Check the avatar ``member`` has.

        `member` **->** The member that you want to see the avatar of. If you want to see your own avatar, you can ignore this since it defaults to you.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        member = member or ctx.author
        em = disnake.Embed(colour=utils.blurple, title=f'`{member.display_name}`\'s avatar')
        em.set_image(url=member.display_avatar)
        em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')
        await ctx.better_reply(embed=em)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def created(self, ctx: Context, *, user: disnake.User = None):
        """Check the date when the ``user`` created their account.

        `user` **->** The user that you want to see the date of when they created their discord account. If you want to see your own account creation date, you can ignore this since it defaults to you.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """  # noqa

        if await ctx.check_channel() is False:
            return

        user = user or ctx.author
        em = disnake.Embed(
            colour=utils.blurple,
            title='Creation Date',
            description=f'{user.mention} created their account '
                        f'on {utils.format_dt(user.created_at, "F")} '
                        f'(`{utils.human_timedelta(user.created_at, accuracy=6)}`)'
        )
        if user.id in [m.id for m in ctx.vystalia.members if not m.bot]:
            sorted_users: list[disnake.Member] = sorted(ctx.vystalia.members, key=lambda m: m.created_at)
            users_ids = [u.id for u in sorted_users]
            pos = users_ids.index(user.id) + 1
            em.set_footer(text=f'{utils.format_position(pos)} oldest account in this server')
        await ctx.better_reply(embed=em)

    @created.command(name='server')
    async def created_server(self, ctx: Context):
        """
        See the date when the server got created at and when it was made public.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        created_date = ctx.vystalia.created_at
        publiced_date = ctx.vystalia.get_member(302050872383242240).joined_at
        members = [m for m in ctx.vystalia.members if not m.bot]
        em = disnake.Embed(colour=utils.red, title='Server Creation')
        em.add_field(
            name='Created At',
            value=f'{utils.format_dt(created_date, "F")} '
                  f'(`{utils.human_timedelta(created_date, accuracy=6)}`)',
            inline=False
        )
        em.add_field(
            name='Publiced At',
            value=f'{utils.format_dt(publiced_date, "F")} '
                  f'(`{utils.human_timedelta(publiced_date, accuracy=6)}`)',
            inline=False
        )
        em.set_footer(text=f'There are currently {len(members)} members in the server')
        await ctx.better_reply(embed=em)

    @commands.command()
    async def joined(self, ctx: Context, *, member: disnake.Member = None):
        """Check the date when the ``member`` joined the server.

        `member` **->** The member that you want to see the date of when they joined this server. If you want to see your own join date, you can ignore this since it defaults to you.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """  # noqa

        if await ctx.check_channel() is False:
            return

        member = member or ctx.author
        em = disnake.Embed(
            colour=utils.blurple,
            title='Join Date',
            description=f'{member.mention} joined the server '
                        f'on {utils.format_dt(member.joined_at, "F")} '
                        f'(`{utils.human_timedelta(member.joined_at, accuracy=6)}`)'
        )
        sorted_users: list[disnake.Member] = sorted(ctx.vystalia.members, key=lambda m: m.joined_at)
        users_ids = [u.id for u in sorted_users if not u.bot]
        pos = users_ids.index(member.id) + 1
        em.set_footer(text=f'Join Position: {utils.format_position(pos)}')
        await ctx.better_reply(embed=em)

    @commands.command(name='membercount', aliases=('memberc', 'mcount', 'mc',))
    async def member_count(self, ctx: Context):
        """Shows how many members the server has, as well as how many are verified and how many are not."""

        members = len([m for m in ctx.vystalia.members if not m.bot])
        bots = len([b for b in ctx.vystalia.members if b.bot])
        verified = len(await self.bot.db.find('intros'))
        unverified = members - verified

        verified_percentage = round(float(verified * 100 / members), 2)
        unverified_percentage = round(float(unverified * 100 / members), 2)

        em = disnake.Embed(title='Member Count', color=utils.blurple)
        em.add_field(
            name='Total Members',
            value=f'{members:,}',
            inline=False
        )
        em.add_field(
            name='Total Bots',
            value=f'{bots:,}',
            inline=False
        )
        em.add_field(
            name='Verified Members',
            value=f'{verified:,} ({verified_percentage}%)',
            inline=False
        )
        em.add_field(
            name='Unverified Members',
            value=f'{unverified:,} ({unverified_percentage}%)',
            inline=False
        )
        em.set_footer(text=f'Requested by: {utils.format_name(ctx.author)}')

        await ctx.better_reply(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.guild.id != 1102654728350998542:
            return

        await self.bot.db.delete('afks', {'_id': member.id})

    @commands.command(name='checkmute', aliases=('checkmutes', 'mutescheck', 'mutecheck',))
    async def check_mute(self, ctx: Context, *, member: disnake.Member = None):
        """
        Check all the current muted members and their time left. If ``member`` is specified, it will only show for that member, including the reason they got muted.

        `member` **->** The member you wish to see the current mute of. If not specified, shows all the currently muted members.
        """  # noqa

        if isinstance(ctx.channel, disnake.DMChannel):
            member = ctx.author

        if member is None:
            entries = []
            index = 0
            for mute in await self.bot.db.find('mutes', {'is_muted': True}):
                mute: Mutes
                if mute.muted is False:
                    continue

                index += 1
                key = ctx.vystalia.get_member(mute.id)
                if key is None:
                    key = f'[LEFT] {mute.id}'

                if mute.permanent is True:
                    _duration = 'PERMANENT'
                    expire_date = 'PERMANENT'
                    remaining = 'PERMANENT'
                else:
                    _duration = mute.duration
                    expire_date = utils.format_dt(mute.muted_until, "F")
                    remaining = utils.human_timedelta(mute.muted_until, suffix=False, accuracy=6)

                value = f'**Muted By:** {ctx.vystalia.get_member(mute.muted_by)}\n' \
                        f'**Reason:** {mute.reason}\n' \
                        f'**Mute Duration:** `{_duration}`\n' \
                        f'**Expires At:** {expire_date}\n' \
                        f'**Remaining:** `{remaining}`\n\n'
                entries.append((f'`{index}`. {key}', value))
            if len(entries) == 0:
                return await ctx.reply(f'{ctx.denial} There are no current mutes.')

            source = FieldPageSource(entries, per_page=5)
            source.embed.color = utils.blurple
            source.embed.title = 'Here are all the currently muted members'
            paginator = RoboPages(source, ctx=ctx, compact=True)
            await paginator.start()
        else:
            mute: Mutes = await self.bot.db.get('mutes', member.id)
            if mute is None or mute.muted is False or mute.is_muted is False:
                if member == ctx.author:
                    return await ctx.reply(f'{ctx.denial} You are not muted.')
                else:
                    return await ctx.better_reply(f'{ctx.denial} `{utils.format_name(member)}` is not muted.')

            em = disnake.Embed(colour=utils.blurple)
            em.set_author(name=utils.format_name(member), icon_url=member.display_avatar)

            if mute.permanent is True:
                _duration = 'PERMANENT'
                expire_date = 'PERMANENT'
                remaining = 'PERMANENT'
            else:
                _duration = mute.duration
                expire_date = utils.format_dt(mute.muted_until, "F")
                remaining = utils.human_timedelta(mute.muted_until, suffix=False, accuracy=6)

            em.description = f'**Muted By:** {ctx.vystalia.get_member(mute.muted_by)}\n' \
                             f'**Reason:** {mute.reason}\n' \
                             f'**Mute Duration:** `{_duration}`\n' \
                             f'**Expires At:** {expire_date}\n' \
                             f'**Remaining:** `{remaining}`'
            em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')
            await ctx.better_reply(embed=em)

    @commands.command(name='checkblock', aliases=('checkblocks', 'blockscheck', 'blockcheck',))
    async def check_block(self, ctx: Context, *, member: disnake.Member = None):
        """
        Check all the current blocked members and their time left. If ``member`` is specified, it will only show for that member, including the reason they got blocked.

        `member` **->** The member you wish to see the current block of. If not specified, shows all the currently blocked members.
        """  # noqa

        if isinstance(ctx.channel, disnake.DMChannel):
            member = ctx.author

        if member is None:
            entries = []
            index = 0
            for block in await self.bot.db.find('mutes', {'is_muted': True}):
                block: Mutes
                if block.blocked is False:
                    continue

                index += 1
                key = ctx.vystalia.get_member(block.id)
                if key is None:
                    key = f'[LEFT] {block.id}'

                if block.permanent is True:
                    _duration = 'PERMANENT'
                    expire_date = 'PERMANENT'
                    remaining = 'PERMANENT'
                else:
                    _duration = block.duration
                    expire_date = utils.format_dt(block.muted_until, "F")
                    remaining = utils.human_timedelta(block.muted_until, suffix=False, accuracy=6)

                value = f'**Blocked By:** {ctx.vystalia.get_member(block.muted_by)}\n' \
                        f'**Reason:** {block.reason}\n' \
                        f'**Block Duration:** `{_duration}`\n' \
                        f'**Expires At:** {expire_date}\n' \
                        f'**Remaining:** `{remaining}`\n\n'
                entries.append((f'`{index}`. {key}', value))
            if len(entries) == 0:
                return await ctx.reply(f'{ctx.denial} There are no current blocks.')

            source = FieldPageSource(entries, per_page=5)
            source.embed.color = utils.blurple
            source.embed.title = 'Here are all the currently blocked members'
            paginator = RoboPages(source, ctx=ctx, compact=True)
            await paginator.start()
        else:
            block: Mutes = await self.bot.db.get('mutes', member.id)
            if block is None or block.blocked is False or block.is_muted is False:
                if member == ctx.author:
                    return await ctx.reply(f'{ctx.denial} You are not blocked.')
                else:
                    return await ctx.better_reply(f'{ctx.denial} `{utils.format_name(member)}` is not blocked.')

            if block.permanent is True:
                _duration = 'PERMANENT'
                expire_date = 'PERMANENT'
                remaining = 'PERMANENT'
            else:
                _duration = block.duration
                expire_date = utils.format_dt(block.muted_until, "F")
                remaining = utils.human_timedelta(block.muted_until, suffix=False, accuracy=6)

            em = disnake.Embed(colour=utils.blurple)
            em.set_author(name=utils.format_name(member), icon_url=member.display_avatar)
            em.description = f'**Blocked By:** {ctx.vystalia.get_member(block.muted_by)}\n' \
                             f'**Reason:** {block.reason}\n' \
                             f'**Block Duration:** `{_duration}`\n' \
                             f'**Expires At:** {expire_date}\n' \
                             f'**Remaining:** `{remaining}`'
            em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')
            await ctx.better_reply(embed=em)

    @commands.command(name='staff', aliases=('mods',))
    async def check_staff(self, ctx: Context):
        """Check the staff members current status."""

        message = ""
        all_status = {
            "online": {"users": [], "emoji": "<:status_online:938412200693997600>"},
            "idle": {"users": [], "emoji": "<:status_idle:938412202090696704>"},
            "dnd": {"users": [], "emoji": "<:status_dnd:938412203026055198>"},
            "offline": {"users": [], "emoji": "<:status_offline:938412200157134858>"}
        }

        owner_icon = '<:owner:938486758654476288>'
        mod_icon = '<:moderator:938486811955703818>'
        admin_icon = '<:admin:938486758117638286>'

        for mem in ctx.vystalia.members:
            if utils.StaffRoles.owner in (r.id for r in mem.roles):  # Checks for owner
                if not mem.bot:
                    if len(all_status[str(mem.status)]['users']) == 0:
                        all_status[str(mem.status)]["users"].append(f"**{mem}** {owner_icon}")
                    else:
                        all_status[str(mem.status)]["users"].append(f"<:blank:938412203579674705> **{mem}** {owner_icon}")
            elif utils.StaffRoles.admin in (r.id for r in mem.roles):  # Checks for admin
                if not mem.bot:
                    if len(all_status[str(mem.status)]['users']) == 0:
                        all_status[str(mem.status)]["users"].append(f"**{mem}** {admin_icon}")
                    else:
                        all_status[str(mem.status)]["users"].append(f"<:blank:938412203579674705> **{mem}** {admin_icon}")
            elif utils.StaffRoles.moderator in (r.id for r in mem.roles):  # Checks for mod
                if not mem.bot:
                    if len(all_status[str(mem.status)]['users']) == 0:
                        all_status[str(mem.status)]["users"].append(f"**{mem}** {mod_icon}")
                    else:
                        all_status[str(mem.status)]["users"].append(f"<:blank:938412203579674705> **{mem}** {mod_icon}")

        for entry in all_status:
            if all_status[entry]["users"]:
                usrs = '\n'.join(all_status[entry]['users'])
                message += f"{all_status[entry]['emoji']} {usrs}\n\n"

        await ctx.better_reply(message)

    @commands.group(name='afk', invoke_without_command=True, case_insensitive=True)
    async def _afk(self, ctx: Context, *, reason: str = None):
        """Set yourself on ``AFK``. While being ``AFK``, anybody who pings you will be told by the bot that you are ``AFK`` with the reason you provided.

        `reason` **->** The reason you are ``AFK``. You can set a default by using `!afk default set`. For a list of commands for that, you can type `!help afk default`.
        """  # noqa

        data: AFK = await self.bot.db.get('afk', ctx.author.id)
        if data is None:
            if reason is None:
                return await ctx.reply('You must give the reason!')
            await self.bot.db.add('afks', AFK(
                id=ctx.author.id,
                reason=reason,
                date=ctx.message.created_at,
                message_id=ctx.message.id,
                is_afk=True
            ))

        elif data is not None:
            if data.is_afk is True:
                return await ctx.reply('You are already ``AFK``!')
            reason = f'{reason} | {data.default}' if reason is not None else data.default
            reason = reason.replace('*', '')  # Make sure it doesn't mess with the default bolding of the reason.
            data.reason = reason
            data.date = ctx.message.created_at
            data.message_id = ctx.message.id
            data.is_afk = True
            await data.commit()

        await ctx.reply(f'You are now ``AFK`` **->** **"{reason}"**')

    @_afk.group(name='default', invoke_without_command=True, case_insensitive=True)
    async def _afk_default(self, ctx: Context):
        """See your default ``AFK`` reason, if you set any."""

        data: AFK = await self.bot.db.get('afk', ctx.author.id)
        if data is None or data.default is None:
            return await ctx.reply('You don\'t have a default ``AFK`` reason set!')

        await ctx.reply(f'Your default ``AFK`` reason is: **"{data.default}"**')

    @_afk_default.command(name='set')
    async def _afk_default_set(self, ctx: Context, *, default: str):
        """Sets your default ``AFK`` reason.

        `default` **->** The default reason you want to set for your ``AFK``.
        """

        data: AFK = await self.bot.db.get('afk', ctx.author.id)
        default = default.replace('*', '')  # Make sure it doesn't mess with the default bolding of the reason.
        if data is None:
            await self.bot.db.add('afks', AFK(
                id=ctx.author.id,
                default=default
            ))
        else:
            data.default = default
            await data.commit()

        await ctx.reply(f'Successfully set your default ``AFK`` reason to: **"{default}"**')

    @_afk_default.command(name='remove')
    async def _afk_default_remove(self, ctx: Context):
        """Removes your default ``AFK`` reason."""

        data: AFK = await self.bot.db.get('afk', ctx.author.id)
        if data is None:
            return await ctx.reply('You don\'t have a default ``AFK`` reason set!')
        await self.bot.db.delete('afk', {'_id': data.pk})

        await ctx.reply('Successfully removed your default ``AFK`` reason.')

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        data: AFK = await self.bot.db.get('afk', message.author.id)
        if data is not None:
            if data.is_afk is True and message.id != data.message_id:
                m = await message.reply(
                    'Welcome back! Removed your ``AFK``\nYou have been ``AFK`` '
                    f'since {utils.format_dt(data.date, "F")} '
                    f'(`{utils.human_timedelta(dt=data.date, accuracy=6)}`)'
                )
                if data.default is None:
                    await self.bot.db.delete('afk', {'_id': data.pk})
                else:
                    data.is_afk = False
                    data.reason = None
                    data.date = None
                    data.message_id = None
                    await data.commit()
                return await utils.try_delete(m, delay=30.0)

        for user in message.mentions:
            data: AFK = await self.bot.db.get('afk', user.id)
            if data is not None and data.is_afk is True:
                m = await message.reply(
                    f'**{utils.format_name(user)}** is ``AFK`` **->** **"{data.reason}"** '
                    f'*since {utils.format_dt(data.date, "F")} '
                    f'(`{utils.human_timedelta(dt=data.date, accuracy=6)}`)*')
                await utils.try_delete(m, delay=30.0)

    @utils.run_in_executor
    def search_wiki(self, query):
        return wikipedia.page(query, auto_suggest=False)

    @commands.command(name='wikipedia', aliases=('wiki',))
    async def _wikipedia(self, ctx: Context, *, query: str):
        """Search something on wikipedia.

        `query` **->** What to search on wikipedia for.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        try:
            res: wikipedia.WikipediaPage = await self.search_wiki(query)
        except Exception:
            return await ctx.reply('Failed to find what you were looking for.')

        menu = utils.WikiView(utils.FrontPageSource(), ctx)
        menu.clear_items()
        menu.add_item(utils.WikiSelect(ctx, res))
        menu.fill_items()

        await menu.start(ref=True)

    @commands.command()
    async def urban(self, ctx: Context, *, query):
        """Searches using urban dictionary for the given query.

        `query` **->** What to search for using the urban dictionary.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        url = 'http://api.urbandictionary.com/v0/define'
        resp = await ctx.session.get(url, params={'term': query})
        if resp.status != 200:
            await self.bot._owner.send(
                embed=disnake.Embed(
                    description=f"[`{ctx.command}`]({ctx.message.jump_url}) gave an error:\n\n"
                                f"Query: **{query}**\nStatus: **{resp.status}**\nReason: **{resp.reason}**"
                )
            )
            return await ctx.send('An error occurred. Please try again later.')

        js: dict = await resp.json()
        data = js.get('list', [])
        if not data:
            return await ctx.send('No results found.')

        pages = RoboPages(source=utils.UrbanDictionaryPageSource(data), ctx=ctx, compact=True)
        await pages.start()

    @commands.command(name='choose', aliases=('pick', 'random',))
    async def pick_random_shit(self, ctx: Context, *, choices: str):
        """Have the bot do a random pick from the choices that you give, each choice is separated by a `|`.

        `choices` **->** The choices you want the bot to randomly pick from. Must be more than one and separated by each other with a `|`
        """

        choices = choices.split('|')
        picks = []
        for choice in choices:
            if choice:
                pick = choice.strip()
                picks.append(utils.remove_markdown(pick))
        if len(picks) < 2:
            return await ctx.reply('You need to give more than 1 choice.')

        for i in range(9):
            random.shuffle(picks)
        pick = random.choice(picks)

        await ctx.reply(f'I have randomly chosen `{pick}`')

    @commands.group(
        name='github',
        aliases=('gh', 'git'),
        hidden=True,
        invoke_without_command=True,
        case_insensitive=True)
    async def base_github(self, ctx: Context):
        """Base github command."""

        await ctx.send_help('github')

    @base_github.command(name='source', aliases=('src',))
    async def github_source(self, ctx: Context, *, command: str = None):
        """Get the source on github for a command the bot has.

        `command` **->** The command you want to see. Can either be a prefixed command or a slash command.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        src = utils.GithubSource(self.bot.user.display_avatar)
        if command is not None:
            if command.lower() == 'help':
                pass
            elif command.lower().startswith(('jsk', 'jishaku')):
                url = 'https://github.com/Kraots/jishaku'
                return await ctx.reply(f'Sorry! That is a module\'s command. Here\'s the link to its github repo:\n<{url}>')
            else:
                command = self.bot.get_command(command) or self.bot.get_slash_command(command)
        data = await src.get_source(command)
        await ctx.better_reply(embed=data.embed, view=data.view)

    @base_github.command(name='user', aliases=('usr',))
    async def github_user(self, ctx: Context, *, username: str):
        """Search for a github user's account via its username.

        `username` **->** The user's github name.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        em = await self.github_client.get_user_info(username)
        await ctx.better_reply(embed=em)

    @base_github.command(name='repository', aliases=('repo',))
    async def github_repo(self, ctx: Context, *, repo: str):
        """Search for a github repository via the following format: `RepoOwnerUsername/RepoName`

        `repo` **->** The repo to search for.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        em = await self.github_client.get_repo_info(repo)
        await ctx.better_reply(embed=em)

    @base_github.command(name='pull')
    @utils.is_owner(owner_only=True)
    async def github_pull(self, ctx: Context):
        """Pulls the changes from the repo."""

        with ShellReader('git pull') as reader:
            content = "```" + reader.highlight
            content += f'\n{reader.ps1} git pull\n\n```'

            em = disnake.Embed(description=content)
            m = await ctx.send(embed=em)

            async for line in reader:
                content = content[:-3]
                content += line + '\n```'
                em.description = content
                await m.edit(embed=em)
        content = content[:-3]
        content += '\n[status] Git pull complete.\n```'
        em.description = content

        r = Repo('.')
        self.bot.git_hash = r.head().decode('utf-8')
        r.close()

        await m.edit(embed=em)

    @staticmethod
    @utils.run_in_executor
    def draw_pie(
        males: int,
        trans_males: int,
        females: int,
        trans_females: int,
        other_gender: int
    ) -> disnake.File:
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect='equal'))
        labels = (
            f'Cis Male ({males:,})', f'Trans Male ({trans_males:,})',
            f'Cis Female ({females:,})', f'Trans Female ({trans_females:,})',
            f'Other Gender ({other_gender:,})'
        )
        data = [males, trans_males, females, trans_females, other_gender]

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: f'{pct:.1f}%', textprops=dict(color='w'))
        ax.legend(
            wedges, labels,
            title='Genders',
            loc='center',
            bbox_to_anchor=(1, 0, 0.8, 1)
        )
        plt.setp(autotexts, size=8, weight='bold')
        ax.set_title('Vystalia Gender Stats')

        plt.savefig('gender_stats.png', bbox_inches='tight')
        file = disnake.File('gender_stats.png')
        return file

    @commands.command(name='genderstats', aliases=('genderratio', 'genders', 'gender'))
    async def gender_stats(self, ctx: Context):
        """
        Shows how many cis males/females, how many trans males/females, and how many people of other gender there are in the server, based on their intros.
        """

        females = 0
        males = 0
        trans_females = 0
        trans_males = 0
        other_gender = 0

        for intro in await self.bot.db.find('intros'):
            gender = intro.gender.lower()

            if gender in ('male', 'm', 'boy', 'make'):
                males += 1
            elif gender in ('trans-male', 'trans male'):
                trans_males += 1

            elif gender in ('female', 'f', 'girl'):
                females += 1
            elif gender in ('trans-female', 'trans female'):
                trans_females += 1

            else:
                other_gender += 1

        em = disnake.Embed(color=utils.blurple)
        em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')

        file = await self.draw_pie(males, trans_males, females, trans_females, other_gender)
        em.set_image(file=file)

        await ctx.better_reply(embed=em)

    @commands.command(name='run', aliases=('code',))
    @commands.cooldown(1, 2.0, commands.BucketType.guild)
    async def run_code(self, ctx: Context, *, code: str):
        r"""Runs the code and returns the result, must be in a codeblock with the markdown of the desired language.

        `code` **->** The code to run.

        **Example:**
        \`\`\`language
        code
        \`\`\`

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        matches = utils.LANGUAGE_REGEX.findall(code)
        if not matches:
            rand = (
                'Your code is not wrapped inside a codeblock.',
                'You forgot your codeblock.',
                'Missing the codeblock.',
            )
            return await ctx.reply(random.choice(rand))

        lang = matches[0][0] or matches[0][1]
        if not lang:
            rand = (
                'You did not specify the language markdown in your codeblock.',
                'Missing the language markdown in your codeblock.',
                'Your codeblock is missing the language markdown.',
            )
            return await ctx.reply(random.choice(rand))

        code = matches[0][2]
        await ctx.trigger_typing()
        _res = await self.bot.session.post(
            'https://emkc.org/api/v1/piston/execute',
            json={'language': lang, 'source': code}
        )
        res = await _res.json()
        if 'message' in res:
            em = disnake.Embed(
                title='An error occured while running the code',
                description=res['message']
            )
            return await ctx.reply(embed=em)

        output = res['output']
        if len(output) > 500:
            content = utils.GistContent(f'```{res["language"]}\n' + output + '\n```')
            url = await self.github_client.create_gist(
                content.source,
                description=f'(`{ctx.author.id}` {utils.format_name(ctx.author)}) code result',
                filename='code_output.txt',
                public=False
            )
            msg = await ctx.reply(f'Your output was too long so I sent it to <{url}>')
            data = self.bot.execs.get(ctx.author.id)
            if data is None:
                self.bot.execs[ctx.author.id] = {ctx.command.name: msg}
            else:
                self.bot.execs[ctx.author.id][ctx.command.name] = msg
            return

        em = disnake.Embed(
            title=f'Ran your `{res["language"]}` code',
            color=utils.blurple
        )
        output = output[:500].strip()
        lines = output.splitlines()
        shortened = (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * '\n\n**Output shortened**'
        em.add_field(name='Output', value=output or '**<No output>**')

        msg = await ctx.reply(embed=em)
        data = self.bot.execs.get(ctx.author.id)
        if data is None:
            self.bot.execs[ctx.author.id] = {ctx.command.name: msg}
        else:
            self.bot.execs[ctx.author.id][ctx.command.name] = msg

    @commands.command(name='time', aliases=('tz', 'timezone'))
    async def user_time(self, ctx: Context, *, member: disnake.Member = None):
        """See what the time is for a user. They must have their birthday set for this to work.

        `member` **->** The member that you want to see the current time of. If you want to see your own time, you can ignore this since it defaults to you.
        """

        member = member or ctx.author
        data: Birthday = await self.bot.db.get('bday', member.id)
        if data is None:
            if member.id == ctx.author.id:
                return await ctx.reply('You must set your birthday if you want to see your current time.')
            else:
                return await ctx.reply(f'{member.mention} must set their birthday first.')

        tz = pytz.timezone(data.timezone.replace(' ', '_'))
        now = datetime.now()
        offset = tz.utcoffset(now) + now
        res = offset.strftime('%d %B %Y, %I:%M %p (%H:%M)')

        em = disnake.Embed(title=f'`{member.display_name}`\'s time information', color=utils.blurple)
        em.add_field('Current Time', res, inline=False)
        em.add_field('Timezone', data.timezone, inline=False)
        em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')

        await ctx.better_reply(embed=em)

    @commands.group(name='calculator', aliases=('calc',), invoke_without_command=True, case_insensitive=True)
    async def calculator_(self, ctx: Context, *, expression: str):
        """Do some math.

        `expression` **->** The expresion you want to calculate (e.g: 1 + 1, etc...)

        **Functions:**
        \u2800 • `sqrt`
        \u2800 • `sin`
        \u2800 • `cos`
        \u2800 • `tan`
        \u2800 • `ceil`
        \u2800 • `floor`
        \u2800 • `sinh`
        \u2800 • `cosh`
        \u2800 • `tanh`
        \u2800 • `abs`
        \u2800 • `log`
        """

        if self.bot.calc_ternary is False:
            return

        operators = r'\+\-\/\*\(\)\^\÷\%\×\.'

        if not any(m in expression for m in operators):
            return await ctx.reply(f'{ctx.denial} Found an operator that doesn\'t exist.')

        for key, value in {
            '^': '**',
            '÷': '/',
            ' ': '',
            '×': '*',
        }.items():
            expression = expression.replace(key, value)

        try:
            # Syntax:
            # 1. See if at least one function or one statement (E.g 1+2) exists, else return
            # 2. Parentheses multiplication is a valid syntax in math, so substitute `<digit*>"("` with `<digit*>"*("`
            # 3. It is possible that the first character in the equation is either "-", "+", or "(", so include it
            # 4. Functions is implemented here, so with functions the syntax would be `[<func>"("<expr*>")"]`
            # 5. Multiple parent/operators also possible, so we do `<digit*>[operators*][digit*]`, operators as wildcard
            # 6. Get the first match of all possible equations
            regex = re.compile(rf"(\d+|{'|'.join(list(functions.keys()))})[{operators}]+\d+")
            match = re.search(regex, expression)
            if not match:
                return

            def parse(_match):
                return _match.group().replace("(", "*(")

            expression = re.sub(re.compile(r"\d\("), parse, expression)
            funcs = "|".join(list(functions.keys()))
            regex = re.compile(
                rf"((([{operators}]+)?({funcs})?([{operators}]+)?(\d+[{operators}]+)*(\d+)([{operators}]+)?)+)"
            )
            match = re.findall(regex, expression)
            content = match[0][0]
            if not any(m in content for m in operators) or not content:
                return await ctx.reply(f'{ctx.denial} Your expression doesn\'t contain any valid operators.')

        except AttributeError:
            return await ctx.reply(f'{ctx.denial} Expression invalid.')

        em = disnake.Embed(color=utils.blurple)
        em.add_field(
            name=f'`{ctx.author.display_name}`\'s calculator',
            value=f'```yaml\n"{content}"\n```',
            inline=False
        )

        try:
            result = simpleeval.simple_eval(content, functions=functions)
            em.add_field(
                name='Result: ',
                value=f'```\n{result}\n```'
            )

        except ZeroDivisionError:
            em.add_field(
                name='Wow...you make me question my existance',
                value='```yaml\nImagine you have zero cookies and you split them amongst 0 friends, '
                      'how many cookies does each friend get? See, it doesn\'t make sense and Cookie Monster '
                      'is sad that there are no cookies, and you are sad that you have no friends.```'
            )
        except SyntaxError:
            return await ctx.reply(f'{ctx.denial} Expression invalid.')
        except simpleeval.NumberTooHigh:
            return await ctx.reply(f'{ctx.denial} Number too high.')
        except Exception:
            return await ctx.reply(f'{ctx.denial} Expression invalid.')
        try:
            await ctx.better_reply(embed=em)
        except disnake.HTTPException:
            return await ctx.reply(f'{ctx.denial} The result of your operation was too long.')

    @calculator_.command(name='toggle')
    @utils.is_owner()
    async def calculator_toggle(self, ctx: Context):
        """
        Toggles whether to use the calculator command or not.

        If disabled, then the calculator command will be disabled and it will evaluate any message's content where it finds an expression.
        """

        ternary = self.bot.calc_ternary
        data: utils.Constants = await self.bot.db.get('constants')
        if ternary is False:
            self.bot.calc_ternary = True
            data.calculator_ternary = True
        else:
            self.bot.calc_ternary = False
            data.calculator_ternary = False
        await data.commit()

        await ctx.reply(
            f'Successfully **{"enabled" if self.bot.calc_ternary is True else "disabled"}** '
            f'the calculator command and **{"disabled" if self.bot.calc_ternary is True else "enabled"}** '
            'checking for expressions in messages automatically.'
        )

    @commands.command()
    async def emojify(self, ctx: Context, *, sentence: str):
        """Emojifies the letters into emojis.

        `sentence` **->** The sentence to emojify.
        """

        _sentence = sentence.lower()
        _sentence = ' '.join(_sentence.split())
        sentence = ''
        for letter in _sentence:
            space = 1
            if letter == ' ':
                space = 3
            sentence += letter + (' ' * space)
        sentence = sentence.translate(utils.LETTERS_TABLE)
        sentence = sentence.translate(utils.NUMBERS_TABLE)

        await ctx.reply(sentence)

    @commands.command(name='mirror')
    async def _mirror_(self, ctx: Context, *, user: disnake.User = None):
        """Invert someone's avatar.

        `user` **->** The user that you want to see the mirrored avatar of. If you want to mirror your own avatar, you can ignore this since it defaults to you.
        """

        user = user or ctx.author
        av = await utils.mirror_avatar(user)
        em = disnake.Embed(title=f'Mirrored `{utils.format_name(user)}`', color=utils.blurple)
        em.set_image(file=av)
        em.set_footer(text=f'Requested By: {utils.format_name(ctx.author)}')
        await ctx.better_reply(embed=em)

    @commands.command(name='quote')
    async def anime_quote(self, ctx: Context):
        """Get a random anime quote."""

        data = await self.bot.session.get('https://animechan.vercel.app/api/random')
        js = await data.json()
        em = disnake.Embed(title='Random anime quote', color=utils.blurple)
        em.add_field('Anime', js['anime'], inline=False)
        em.add_field('Character', js['character'], inline=False)
        em.add_field('Quote', js['quote'], inline=False)

        await ctx.reply(embed=em)

    @commands.command(name='roast')
    async def roast_cmd(self, ctx: Context, *, member: disnake.Member = None):
        """Roast someone or yourself.

        `member` **->** The member you want to roast. Defaults to yourself.
        """

        member = member or ctx.author
        if member == ctx.author:
            fmt = f'{ctx.author.mention} Hah! You roasted yourself.'
        else:
            if member.id == self.bot._owner_id:
                fmt = f'{ctx.author.mention} you got roasted by {self.bot._owner.mention}'
                member = ctx.author
            else:
                fmt = f'{member.mention} you got roasted by {ctx.author.mention}'

        data = await self.bot.session.get('https://insult.mattbas.org/api/insult')
        roast = (await data.read()).decode()
        roast = roast + '.' if not roast.endswith('.') else roast
        em = disnake.Embed(
            title=f'`{utils.format_name(member)}` get roasted',
            description=roast,
            color=utils.blurple
        )

        await ctx.reply(fmt, embed=em)

    @commands.command(name='boosters', aliases=('booster', 'kitties'))
    async def check_boosters(self, ctx: Context):
        """See all the kitties that are currently boosting the server, in order based on the date they started boosting.

        **NOTE:** This command can only be used in <#1102654729387004047>
        """

        if await ctx.check_channel() is False:
            return

        boosters = []
        sorted_ = sorted(ctx.vystalia.premium_subscribers, key=lambda m: m.premium_since)
        for index, member in enumerate(sorted_):
            boosters.append(
                (
                    f'`#{index + 1}` {utils.format_name(member)}',
                    f'{member.mention} Has been boosting this server since '
                    f'{utils.format_dt(member.premium_since, "F")} '
                    f'(`{utils.human_timedelta(member.premium_since)}`)\n _ _ '
                )
            )

        source = utils.FieldPageSource(boosters, per_page=5)
        source.embed.color = utils.booster_pink
        source.embed.title = 'Here\'s all the kitties of `Vystalia`'
        pag = utils.RoboPages(source, ctx=ctx, compact=True)
        await pag.start(ref=True)

    @commands.command(name='reverseimagesearch', aliases=('reverseimage', 'reverse', 'imagesearch'))
    async def reverse_image_search(self, ctx: Context, *, url: str = None):
        """Do a reverse image search with the google's reverse image search engine from the given url.

        `url` **->** The url with the image to search for. It's optional and if you don't give it but reply to a message instead it will firstly try to get the first attachment from that image, and if not found it will try looking for links in that message.
        """  # noqa

        if url is None:
            if ctx.replied_reference is not None:
                reference = await self.bot.reference_to_message(ctx.replied_reference)
                if reference:
                    if reference.attachments:
                        url = reference.attachments[0].url
                    else:
                        res = utils.URL_REGEX.findall(reference.content)
                        if res:
                            for u in res:
                                if u.endswith(('.png', '.gif', '.jpeg', '.jpg')):
                                    url = u
                                    break
            else:
                return await ctx.reply('You must either give the url or reply to a message.')

        search = GoogleSearch(dict(
            engine='google_reverse_image',
            image_url=url,
            api_key=self.bot.serpapi_key
        ))
        result = search.get_dict()
        image = result.get('inline_images')
        if image is None:
            return await ctx.reply('Could not find an image.')
        await ctx.reply(
            embed=disnake.Embed(
                title='Match found',
                description=f'Click [`here`]({image[0]["link"]}) to see your reverse image search result.',
                color=utils.blurple
            )
        )

    @commands.command(name='enlarge', aliases=('ee',))
    async def enlarge_emoji(self, ctx: Context, emojis: commands.Greedy[disnake.PartialEmoji]):
        """Enlarges the given emojis. Can be either one or more.

        `emoji` **->** The emojis to enlarge. It's optional and you can also reply to a message with this command to get the emojis from that message.
        **NOTE:** This works for custom emojis only!
        """

        if len(emojis) == 0:
            if ctx.replied_reference is not None:
                reference = await self.bot.reference_to_message(ctx.replied_reference)
                if reference:
                    _emojis = utils.CUSTOM_EMOJI_REGEX.findall(reference.content)
                    if _emojis:
                        for emoji in _emojis:
                            animated = True if emoji[0] != '' else False
                            emojis.append(disnake.PartialEmoji(name=emoji[1], id=emoji[2], animated=animated))
            else:
                return await ctx.reply('Must either give the emojis either reply to a message that has them.')

        if len(emojis) == 0:
            return await ctx.reply('No emojis found.')

        embeds = []
        for emoji in emojis:
            embed = disnake.Embed(
                title=f'Showing emoji `{emoji.name}`',
                color=utils.blurple
            )
            embed.set_image(emoji.url)
            embeds.append(embed)

        paginator = utils.EmbedPaginator(ctx, embeds)
        await paginator.start(ref=True)


def setup(bot: Vystalia):
    bot.add_cog(Misc(bot))
