import discord
from discord.ext import commands
import json
import asyncio

def noMD(str):
    return str.replace("*", "").replace("_", "").replace("@everyone","Everyone").replace("@here","Here").replace("://", ";//")

def setup(bot):
    bot.add_cog(Embed(bot))

    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.embeds and reaction.message.author.id == bot.user.id:
            neededCount = int(reaction.message.embeds[0].title[7:-26])

            if(reaction.count > neededCount):
                em = discord.Embed(title=f"Vote - {reaction} won!", description=reaction.message.embeds[0].description, color=bot.color)
                em.set_author(name=reaction.message.embeds[0].author.name, icon_url=reaction.message.embeds[0].author.icon_url)
                em.set_footer(text=bot.user.name, icon_url=bot.icon)
                await reaction.message.edit(embed=em)

class Embed(commands.Cog, name="Embed"):
    """
    Create custom embeds with ease!
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def em(self, ctx, title, *, text):
        """Create an embed with a custom title and body."""
        em = discord.Embed(title=noMD(title), description=noMD(text), color=self.bot.color)
        em.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        await ctx.channel.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def emAdv(self, ctx, title, text, *, Color):
        """Create an embed with a custom title, body, and color"""
        em = discord.Embed(title=title, description=text, color=int(Color, 16))
        em.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        await ctx.channel.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def emPro(self, ctx, title, text, Color, authorName, *, authorURL):
        """Create an embed with a custom title, body, color, and author data."""
        em = discord.Embed(title=title, description=text, color=int(Color, 16))
        em.set_author(name=authorName, icon_url=authorURL)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        await ctx.channel.send(embed=em)

    @commands.command(aliases=["poll", "democracy", "yn"])
    async def vote(self, ctx, votesNeeded : int, *, proposal):
        """Start a yes/no vote."""
        channel = ctx.message.channel
        em = discord.Embed(title=f"Vote - {votesNeeded} votes on one side needed.", description=noMD(proposal), color=self.bot.color)
        em.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        embd = await ctx.channel.send(embed=em)
        msg = await ctx.fetch_message(embd.id)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(aliases=["choose", "mc"])
    async def choice(self, ctx, votesNeeded : int, optionCount : int, *, proposal):
        """Start a multiple-choice vote."""
        channel = ctx.message.channel
        em = discord.Embed(title=f"Vote - {votesNeeded} votes on one side needed.", description=noMD(proposal), color=self.bot.color)
        em.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
        await ctx.message.delete()
        embd = await ctx.channel.send(embed=em)
        msg = await ctx.fetch_message(embd.id)
        org = "\U0001F1E6"

        if optionCount < 2:
            optionCount = 2

        if votesNeeded < 1:
            votesNeeded = 1

        for i in range(0, int(optionCount)):
            if i % 20 == 0 and i > 0:
                em = discord.Embed(title=f"Vote - {votesNeeded} votes on one side needed.", description=noMD(proposal), color=self.bot.color)
                em.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
                embd = await ctx.channel.send(embed=em)
                msg = await ctx.fetch_message(embd.id)
                optionCount = str(0)
            
            if i == 21:
                if ctx.message.author.id in self.bot.trustedUsers:
                    org = "\U0001F600"
                else:
                    await ctx.channel.send("(btw you're insane.)")
                    break

            if i == 80:
                org = "\U0001F400"

            if i == 254:
                await ctx.channel.send("(btw you're *really* insane.)")
                break

            await msg.add_reaction(str(chr(ord(org) + i)))