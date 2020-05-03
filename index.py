#!/usr/bin/env python3

# Cathode
# A simplistic modular Discord bot by Shuga

import os
import importlib
import discord
from discord.ext import commands
import asyncio
import datetime
import json
import datetime
import psutil, sys

# Little code borrowed from LapisMirror.
with open("config.json") as config_file:
    config = json.load(config_file)

# Toggle debug mode. Should be False on prod.
__debugMode__ = False

__version__ = config["version"]
__token__ = config["token"]
__prefix__ = config["prefix"]
__gamePlaying__ = config["gamePlaying"]
__color__ = int(config["color"], 16)
__perms__ = "36826176"

try:
    __verified__ = config["verified"]
except:
    __verified__ = False

"""
A set of aux debug functions to make things clean.
"""
class log:
    def success(txt):  # Used for successful operations.
        print(f"\033[92m{txt}\033[0m")

    def debug(txt):  # Used for debugging.
        if(__debugMode__):
            print(f"\033[94m{txt}\033[0m")

    def warning(txt):
        print(f"\033[93m{txt}\033[0m")

    def error(txt):
        print(f"\033[91m{txt}\033[0m")

    def info(txt):
        print(f"\033[95m{txt}\033[0m")

    def head(txt):
        print(f"\033[95m\033[1m{txt}\033[0m")

"""
The next commands are for creating embeds.
"""
def createEmbed():
    em = discord.Embed(color=__color__)
    return em

def createEmbedCustomColor(color):
    em = discord.Embed(color=color)
    return em

def createTextEmbed(title, desc):
    em = discord.Embed(title=title, description=desc, color=__color__)
    return em

def errorCommand(self, text):
    em = discord.Embed(color=__color__)
    em.add_field(name="Error", value=text)
    em.set_footer(text=self.user.name, icon_url=f"https://cdn.discordapp.com/avatars/{self.user.id}/{self.user.avatar}.png?size=512")
    return em

def badCommandError(self, ctx, error, desc):
    signature = ctx.command.signature
    if desc != "":
        signature = f"{signature}\n\n**Error: {desc}**"
    else:
        signature = signature.replace(f"<{str(error.param).split(':', 1)[0]}>", f"**<{str(error.param).split(':', 1)[0]}>**")
    em = createTextEmbed("Help", f"{__prefix__}{ctx.command.name} {signature}")
    em.add_field(name="**Description**", value=ctx.command.help, inline=False)
    em.set_footer(text=self.user.name, icon_url=f"https://cdn.discordapp.com/avatars/{self.user.id}/{self.user.avatar}.png?size=512")
    return em

"""
Get uptime of bot.
"""
def get_bot_uptime(self, *, brief=False):
    # Courtesy of Danny
    now = datetime.datetime.utcnow()
    delta = now - self.bot.uptime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if not brief:
        if days:
            fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h} hours, {m} minutes, and {s} seconds'
    else:
        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

"""
The main bot.
"""
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = __prefix__,
            help_command = None
        )

        self.remove_command("help")

        self.add_cog(CathodeHelpCommand(self))
        self.add_cog(Core(self))

        pluginFolder = os.listdir("cogs")

        self.color = __color__
        self.cathodeVersion = __version__
        self.gamePlaying = __gamePlaying__
        # Once the bot starts, the following properties will be swapped for the correct ones.
        self.trustedUsers = sorted(config["admins"])
        self.icon = "https://discordapp.com/assets/dd4dbc0016779df1378e7812eabaa04d.png"

        # Load external cogs
        for i in pluginFolder:
            if ((i.endswith(".py") and "__" not in i) or (i.endswith(".py3") and "__" not in i)):
                self.load_extension(f"cogs.{os.path.splitext(i)[0]}")
                log.debug(f"Plugin loaded: {i}...")

    # async def on_command(self, ctx):
    #     await ctx.channel.trigger_typing()

    # async def on_command_completion(self, ctx):
    #     print("do nothing...")

    async def on_guild_join(self, guild):
        # Warn you when your bot isn't verified and is about to hit the non-verified limit.
        count = 0
        for guild in self.guilds:
            count += 1

        if count >= 100 and __verified__.lower() == "true":
            ownerChannel = self.get_user(int(config["owner"]))
            em = createTextEmbed(
                f"Verification Warning",
                f"Your bot, {self.user.name}, is currently in {count} servers. \
                You cannot join any more servers without being verified. \nIf you are already \
                verified, set `verified` to `true` in `config.json`."
                )
            em.add_field(name="Get Started", value=f"[Developer Portal](https://discordapp.com/developers/applications/{str(self.user.id)}/bot)")
            em.set_footer(text=self.user.name, icon_url=self.bot.icon)
            await ownerChannel.send(embed=em)
        elif count >= 75 and count % 5 == 0 and __verified__.lower() == "true":
            ownerChannel = self.get_user(int(config["owner"]))
            em = createTextEmbed(
                f"Verification Warning",
                f"Your bot, {self.user.name}, is currently in {count} servers. \
                That's dangerously close to the 100 server limit that Discord allows for \
                non-verified bots. Consider applying for verification as soon as possible. \n\
                If you are already verified, set `verified` to `true` in `config.json`."
                )
            em.add_field(name="Get Started", value=f"[Developer Portal](https://discordapp.com/developers/applications/{str(self.user.id)}/bot)")
            em.set_footer(text=self.user.name, icon_url=self.bot.icon)
            await ownerChannel.send(embed=em)

    async def on_ready(self):
        # This is going to be used elsewhere.
        data = await self.application_info()
        self.owner_id = data.owner.id

        # Owner is admin by default.
        arr = config["admins"] + [self.owner_id]

        self.trustedUsers = sorted(arr)
        self.icon = f"https://cdn.discordapp.com/avatars/{self.user.id}/{self.user.avatar}.png?size=512"

        own = data.owner

        log.info(f"Instance owned by @{own.name}#{own.discriminator}")
        log.success(f"Logged in as {self.user.name} ({str(self.user.id)})")
        log.info(f"To add {self.user.name} to your server, go to \033[1mhttps://discordapp.com/oauth2/authorize?client_id={str(self.user.id)}&scope=bot&permissions={__perms__}")
        await self.change_presence(status=discord.Status.online, activity=discord.Game(__gamePlaying__))
        # Log launch time.
        self.uptime = datetime.datetime.utcnow()

    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send(embed=badCommandError(self, ctx, error, ""))
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send(embed=badCommandError(self, ctx, error, "The parameters given were not valid."))
        elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
            await ctx.channel.send(embed=errorCommand(self, f"The command **{__prefix__}{ctx.command.name}** cannot be used in direct messages."))
        elif isinstance(error, discord.ext.commands.errors.DisabledCommand):
            await ctx.channel.send(embed=errorCommand(self, f"The command **{__prefix__}{ctx.command.name}** is disabled."))
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(embed=errorCommand(self, f"You don't have permission to run this command on this server."))
        elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            await ctx.channel.send(embed=errorCommand(self, f"I am missing some permissions! Please have the server moderators give me any needed permissions."))
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.channel.send(embed=errorCommand(self, f"Something went wrong when running that command. Please contact the bot owner with `{__prefix__}message` to report this."))
        elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.channel.send(embed=errorCommand(self, error))
        else:
            if __debugMode__:
                await ctx.channel.send(embed=errorCommand(self, f"{error}\n\n*(You're seeing this message because Debug Mode is enabled.)*"))
            else:
                await ctx.channel.send(embed=errorCommand(self, f"Something went horribly wrong. Please contact the bot owner with `{__prefix__}message` to report this."))

        if ctx.command:
            log.debug(f"Command {__prefix__}{ctx.command.name} erred: {error}")
        else:
            log.debug(f"Bot erred: {error}")

class CathodeHelpCommand(commands.Cog, name="Help"):
    """
    Learn how to use the bot
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(hidden=True)
    async def help(self, ctx, cog_name=None):
        """Learn how to use the bot."""
        Cog = self.bot.get_cog(cog_name)
        field_count = 1

        if Cog == None:
            em = createEmbed()
            em.set_author(name=f"Commands for {self.bot.user.name}", icon_url=self.bot.icon)
            em.add_field(name="About", value=config["about"], inline=False)
            for el in self.bot.cogs:
                # Make sure embed is short enough. If it isn't, make another.
                if field_count > 10:
                    await ctx.channel.send(embed=em)
                    em = createEmbed()
                    field_count = 0
                if el.lower() != "help":
                    subCog = self.bot.get_cog(el)
                    em.add_field(name=f"**{subCog.qualified_name}**", value=subCog.description, inline=False)
                    field_count = field_count + 1
                    for x in subCog.get_commands():
                        field_count = field_count + 1
                        if x.hidden == False:
                            em.add_field(name=f"{__prefix__}{x.name}", value=x.help, inline=True)
            em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
            await ctx.channel.send(embed=em)
        else:
            em = createEmbed()
            em.set_author(name=f"Help for {Cog.qualified_name}", icon_url=self.bot.icon)
            em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
            em.add_field(name="**Description**", value=Cog.description, inline=False)
            for x in Cog.get_commands():
                # Don't reveal commands that are hidden!
                if x.hidden == False:
                    em.add_field(name=f"{__prefix__}{x.name}", value=x.help, inline=True)
            await ctx.channel.send(embed=em)

"""
Core commands to make Cathode work.
"""
class Core(commands.Cog, name="Core"):
    """
    What makes the bot tick.
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def about(self, ctx):
        """Versioning information"""
        own = self.bot.get_user(self.bot.owner_id)

        em = createEmbed()
        em.set_thumbnail(url=self.bot.icon)
        em.add_field(name="Version", value=__version__, inline=True)
        em.add_field(name="discord.py Version", value=str(discord.__version__), inline=True)
        em.add_field(name="Creator", value=f"[@{own.name}#{own.discriminator}]({config['url']})", inline=True)
        em.add_field(name="Add Me!", value=f"[Click Here to Add](https://discordapp.com/oauth2/authorize?client_id={str(self.bot.user.id)}&scope=bot&permissions={__perms__})", inline=True)
        em.add_field(name="Source Code", value="[View Source](https://github.com/Shugabuga/Cathode)", inline=True)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.channel.send(embed=em)

    @commands.command(hidden=True)
    async def amITrusted(self, ctx):
        """Trusted status of user."""
        if ctx.message.author.id in self.bot.trustedUsers:
            await ctx.channel.send("You are an admin of this bot.")
        else:
            await ctx.channel.send("You are not an admin of this bot.")

    @commands.command()
    async def add(self, ctx):
        """Add the bot to your server."""
        em = createTextEmbed("Add Me!", "")
        em.add_field(
            name=f"Add {self.bot.user.name} to your server",
            value=f"[Click Here to Add](https://discordapp.com/oauth2/authorize?client_id={str(self.bot.user.id)}&scope=bot&permissions={__perms__})",
            inline=True
        )
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.channel.send(embed=em)

    @commands.command()
    async def message(self, ctx, *, text):
        """Send a message to the bot's operator."""
        ownerChannel = self.bot.get_user(int(config["owner"]))

        if ctx.guild:
            footer = f"{self.bot.user.name} | Server ID: {str(ctx.guild.id)} | User ID: {str(ctx.author.id)}"
            srvName = ctx.guild.name
            await ctx.author.create_dm()
        elif ctx.author.dm_channel:
            footer = f"{self.bot.user.name} | Server ID: {str(ctx.author.dm_channel.id)} | User ID: {str(ctx.author.id)}"
            srvName = f"{ctx.author.name}'s DMs"
        else:
            footer = f"{self.bot.user.name} | Server ID: Unknown | User ID: {str(ctx.author.id)}"
            srvName = "a server"

        em = createTextEmbed(f"From {srvName}", text)
        em.add_field(name="Reply", value=f"[Reply to User](https://discordapp.com/channels/@me/{str(ctx.author.dm_channel.id)})")
        em.set_author(name=f"@{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        em.set_footer(text=footer, icon_url=self.bot.icon)
        await ownerChannel.send(embed=em)

    @commands.command(aliases=["latency", "pong"])
    async def ping(self, ctx):
        """Check the bot's latency."""
        await ctx.channel.send(f"{self.bot.user.name} is working and is on version {__version__} and has a latency of {str(self.bot.latency)}.")

    @commands.command()
    async def uptime(self, ctx):
        """Check the bot's uptime."""
        since = self.bot.uptime.strftime("%Y-%m-%d %H:%M:%S")
        passed = get_bot_uptime(self)
        em = createTextEmbed("Uptime", f"Been online for **{format(passed)}** (since {format(since)}) UTC.")
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.channel.send(embed=em)

    @commands.command(hidden=True)
    async def restart(self, ctx):
        """Restart the bot."""
        if ctx.message.author.id in self.bot.trustedUsers:
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("Restarting..."))
            await ctx.channel.send("Good night! I'll be right back.")
            
            try:
                p = psutil.Process(os.getpid())
                for handler in p.get_open_files() + p.connections():
                    os.close(handler.fd)
            except:
                pass

            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            await ctx.channel.send(embed=errorCommand(self.bot, "You don't have permission to run this command."))

def main():
    log.head("Welcome to Cathode.")

    # Checks
    if(discord):
        log.debug("discord.py loaded successfully.")
    else:
        log.error("discord.py was not loaded.")

    if(config["version"]):
        log.debug("Config file loaded successfully.")
    else:
        log.error("Config file was not loaded.")

    session = Bot()

    # Run stable or beta.
    if  __debugMode__ == True:
       log.info("Version " + __version__ + " (beta)")
       session.run(config["betaToken"])
    else:
        log.info("Version " + __version__ + " (prod)")
        session.run(__token__)

if __name__ == '__main__':
    main()
