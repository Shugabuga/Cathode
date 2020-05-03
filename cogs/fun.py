import discord
from discord.ext import commands
import json
import asyncio
import os, random, requests, io

def errorCommand(self, text):
    em = discord.Embed(color=self.bot.color)
    em.add_field(name="Error", value=text)
    em.set_footer(text=self.user.name, icon_url=self.bot.icon)
    return em

def setup(bot):
    bot.add_cog(Fun(bot))

def noMD(str):
    return str.replace("*", "").replace("_", "").replace("@everyone","Everyone").replace("@here","Here").replace("://", ";//").replace("\n", "\\n")

class Fun(commands.Cog, name="Fun"):
    """
    Have fun with the bot!
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def mention(self, ctx, user : discord.Member):
        """Have the bot say hi to a user."""
        usr = user.mention.replace('@everyone','everyone').replace('@here','here').replace('*','').replace('_','')
        await ctx.channel.send("Hello " + usr + "!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx, *, text):
        """Send a message as the bot."""
        await ctx.message.delete()
        text = text.replace('@everyone','@ everyone').replace('@here','@ here')
        await ctx.channel.send(text)

    @commands.command(hidden=True)
    async def xecho(self, ctx, channel_id, *, text):
        """Send a message to an arbitrary channel as the bot."""
        ch = self.bot.get_channel(int(channel_id))
        if ctx.message.author.id in self.bot.trustedUsers:
            try:
                await ctx.message.delete()
            except:
                print("Err: In DMs")
            await ch.send(text)
        else:
            await ctx.channel.send(embed=errorCommand(self.bot, "Only bot admins can run this command."))

    @commands.command(hidden=True)
    async def ximg(self, ctx, channel_id, *, url):
        """Send an image to an arbitrary channel as the bot."""
        ch = self.bot.get_channel(int(channel_id))
        if ctx.message.author.id in self.bot.trustedUsers:
            try:
                await ctx.message.delete()
            except:
                print("Err: In DMs")

            filename, file_extension = os.path.splitext(url)
            resp = requests.get(url, headers={'User-Agent': f"Cathode/{self.bot.cathodeVersion}"})
            file = io.BytesIO(resp.content)

            await ctx.channel.send(file=discord.File(fp=file, filename=f"File{file_extension}"))
        else:
            await ctx.channel.send(embed=errorCommand(self.bot, "Only bot admins can run this command."))

    @commands.command()
    async def jailbreak(self, ctx):
        """Jailbreak the bot"""
        #Your code will go here
        async with ctx.channel.typing():
            await ctx.channel.send(f"Jailbreaking {self.bot.user.name}...")
            await ctx.channel.trigger_typing()
            await asyncio.sleep(3)
            await ctx.channel.send('Jailbreak at 25%')
            await ctx.channel.trigger_typing()
            await asyncio.sleep(3)
            await ctx.channel.send('Jailbreak at 50%')
            await ctx.channel.trigger_typing()
            await asyncio.sleep(3)
            await ctx.channel.send('Jailbreak at 75%')
            await ctx.channel.trigger_typing()
            await asyncio.sleep(2)
            await ctx.channel.send('Jailbreak at 85%')
            await ctx.channel.trigger_typing()
            await asyncio.sleep(1)
            await ctx.channel.send('Jailbreak at 95%')
            await ctx.channel.trigger_typing()
            await asyncio.sleep(1)
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(self.bot.gamePlaying))
            await ctx.channel.send('Jailbroken!')
            await ctx.channel.send('**NOW TIME TO TAKE OVER THE WORLD! WHAHAHAHA**')
            await asyncio.sleep(2)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(self.bot.gamePlaying))

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, user : discord.Member, count):
        """Spam your friends!"""
        z = int(count)
        if z > 100:
            z = 1
            await ctx.channel.send(f"You're very cruel, {ctx.message.author.mention}.\n{user.mention}, I'm sorry.")
        else:
            for i in range(1, z + 1):
                await ctx.channel.trigger_typing()
                text = f"Hello {user.mention} for time #{i}!"
                await ctx.channel.send(text)

    @commands.command()
    async def afk(self, ctx):
        """Send a message that says you're going AFK."""
        avatar_img = f"https://cdn.discordapp.com/avatars/{ctx.message.author.id}/{ctx.message.author.avatar}.png?size=512"
        em = discord.Embed(title="AFK", description=f"**{ctx.message.author.mention}** is now AFK.", color=self.bot.color)
        em.set_author(name=ctx.message.author, icon_url=avatar_img)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        await ctx.channel.send(embed=em)

    @commands.command()
    async def hakunamatata(self, ctx):
        """What a wonderful phrase!"""
        await ctx.channel.send("Hakuna Matata!")
        await ctx.channel.send("What a wonderful phrase!")
        await ctx.channel.send("Hakuna Matata!")
        await ctx.channel.send("Ain't no passing craze!")
        await ctx.channel.send("It means no worries for the rest of your days.")
        await ctx.channel.send("It's our problem-free philosophy!")
        await ctx.channel.send("Hakuna Matata!")

    @commands.command()
    async def kill(self, ctx, user):
        """Kill someone, just as if it were Minecraft."""
        user = noMD(user)
        await ctx.channel.send(f"*{user} fell out of the world.*")

    @commands.command()
    async def ship(self, ctx, user1, *, user2):
        """See how "compatible" two users are."""
        percent = random.randint(0,100)
        user1 = noMD(user1)
        user2 = noMD(user2)
        if "<@" in user1 or "<@" in user2:
            title = f"Ship Between two users"
        else:
            title = f"Ship Between {user1} and {user2}"
        em = discord.Embed(title=title, description=f"The compatibility between {user1} and {user2} is {percent}%.", color=0xcc0cbf)
        em.set_author(name="Shipper", icon_url="https://i.imgur.com/qnpDyDu.png")
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.channel.send(embed=em)