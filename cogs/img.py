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
    bot.add_cog(Images(bot))

def noMD(str):
    return str.replace("*", "").replace("_", "").replace("@everyone","Everyone").replace("@here","Here").replace("://", ";//").replace("\n", "\\n")

def nekos_life(category):
    """
    A tiny wrapper to return an image from the nekos.life API.
    Returns a DiscordPy file object.
    """
    # Fetch URL via JSON
    url = f"https://nekos.life/api/v2/img/{category}"
    callapi = requests.get(url, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
    json = callapi.json()
    url = json["url"]

    # Get image.
    resp = requests.get(url, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
    file = io.BytesIO(resp.content)
    return discord.File(fp=file, filename=f"{category}.jpeg")

class Images(commands.Cog, name="Images"):
    """
    Get some random images and memes.
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["kitty", "meow"])
    async def cat(self, ctx):
        """Get a picture of a cat."""
        async with ctx.channel.typing():
            url = "https://thecatapi.com/api/images/get?format=src&type=jpg"
            
            # Retrieve file and store it into memeory.
            resp = requests.get(url, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
            file = io.BytesIO(resp.content)

            await ctx.channel.send(file=discord.File(fp=file, filename=f"Cat.jpg"))

    # Cultural note: Yes, I know "neko," "kitsune," and "kemono" translate to the animals themselves
    #                (cat, fox, beast) and not the moe-fied version. However, they're probably
    #                fine as aliases to these commands that are hidden already.

    @commands.command(aliases=["neko", "nya", "cat_girl"], hidden=True)
    async def catgirl(self, ctx):
        """Get a picture of a catgirl."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("neko"))

    @commands.command(aliases=["kitsune", "fox_girl"], hidden=True)
    async def foxgirl(self, ctx):
        """Get a picture of a foxgirl."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("fox_girl"))

    @commands.command(aliases=["spice_and_wolf", "spiceandwolf", "holosan"], hidden=True)
    async def holosama(self, ctx):
        """Get a picture of Holo from Spice and Wolf."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("holo"))

    @commands.command(aliases=["kemono", "beast_girl", "beastgirl", "animal_girl", "animalgirl"], hidden=True)
    async def kemonomimi(self, ctx):
        """Get a picture of a girl with animal ears."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("kemonomimi"))

    @commands.command(aliases=["animewall", "anime_wall", "animewallpaper","aniwall", "ani_wall"], hidden=True)
    async def anime_wallpaper(self, ctx):
        """Get an anime wallpaper."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("wallpaper"))

    @commands.command(aliases=["honk"])
    async def goose(self, ctx):
        """Get a picture of a goose."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("goose"))

    @commands.command()
    async def lizard(self, ctx):
        """Get a picture of a lizard."""
        async with ctx.channel.typing():
            await ctx.channel.send(file=nekos_life("lizard"))

    @commands.command(aliases=["doggo", "puppy", "pupper", "woof", "bark"])
    async def dog(self, ctx):
        """Get a picture of a dog."""
        async with ctx.channel.typing():
            # Fetch URL via JSON
            url = "https://random.dog/woof.json"
            callapi = requests.get(url, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
            json = callapi.json()
            doggo = json["url"]
            # Get file extension and post accordingly
            filename, file_extension = os.path.splitext(doggo)

            # Is it a video?
            if file_extension.lower() == ".mp4":
                resp = requests.get(doggo, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
                video = io.BytesIO(resp.content)
                await ctx.channel.send(file=discord.File(fp=video, filename="Dog.mp4"))
            # Is it a GIF?
            elif file_extension.lower() == ".gif":
                resp = requests.get(doggo, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
                file = io.BytesIO(resp.content)
                await ctx.channel.send(file=discord.File(fp=file, filename="Dog.gif"))
            # Is it a PNG?
            elif file_extension.lower() == ".png":
                resp = requests.get(doggo, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
                file = io.BytesIO(resp.content)
                await ctx.channel.send(file=discord.File(fp=file, filename="Dog.png"))
            else:
                # Upload as JPG
                resp = requests.get(doggo, headers={"User-Agent": f"Cathode/{self.bot.cathodeVersion}"})
                file = io.BytesIO(resp.content)
                await ctx.channel.send(file=discord.File(fp=file, filename="Dog.jpg"))