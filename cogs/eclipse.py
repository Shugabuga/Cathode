import discord
from discord.ext import commands
import json
import asyncio
import requests, re

def getNameKey(obj):
    return obj["Name"]

def noMD(str):
    return str.replace("*", "").replace("_", "").replace("@everyone","Everyone").replace("@here","Here").replace("://", ";//").replace("\n", "\\n")

def create_eclipse_link(url):
    eclipse_regex = r'http(s|):\/\/(.*)\/(.*).(gba|nes|gb|gbc|snes|sms|sgg)(|\?dl=1)'
    parse = re.findall(eclipse_regex, str(url))[0]

    query = parse[2]
    sys = parse[3].lower()
    query = query.replace("_", " ").replace("-", " ").replace("+", " ").replace("%20", " ")

    try:
        req = requests.get(f"https://api.zenithdevs.com/eclipse/boxart/q/{query}")
        resp = req.json()
        resp = resp[sys][0]

        uri = f"https://eclipseemu.me/play/?q=rom&name={resp['name']}&art={resp['boxart']}&url={url}&sys={sys.upper()}"
        return {
            "uri": uri.replace(" ", "%20"),
            "link": url.replace(" ", "%20"),
            "name": resp["name"],
            "img": resp["boxart"].replace(" ", "%20"),
            "sys": sys.upper()
        }
    except:
        uri = f"https://eclipseemu.me/play/?q=rom&name={query}&art=https://eclipseemu.me/play/assets/img/default-cover.png&url={url}&sys={sys.upper()}"
        return {
            "uri": uri.replace(" ", "%20"),
            "link": url.replace(" ", "%20"),
            "name": query,
            "img": "https://eclipseemu.me/play/assets/img/default-cover.png",
            "sys": sys.upper()
        }
    

def setup(bot):
    bot.add_cog(Eclipse(bot))

class Eclipse(commands.Cog, name="Eclipse"):
    """
    Eclipse, a web-based multi-platform emulator. https://eclipseemu.me

    Post a valid link to a supported ROM to get a link to play in-browser.
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        @bot.listen("on_message")
        async def url_textscan(message):
            eclipse_regex = r'http(s|):\/\/(.*)\/(.*).(gba|nes|gb|gbc|snes|sms|sgg)(|\?dl=1)'
            if re.match(eclipse_regex, message.content, re.IGNORECASE) is not None:
                async with message.channel.typing():
                    matches = re.findall(eclipse_regex, str(message.content))[0]

                    res = create_eclipse_link(message.content)

                    em = discord.Embed(title=f"Add \"{res['name']}\"", description=f"Click [**here**]({res['uri']}) to add the above ROM to Eclipse.", color=0xcd1b45)
                    em.set_thumbnail(url=res["img"])
                    em.set_author(name="Eclipse", icon_url="https://eclipseemu.me/play/static/icons/apple-touch-icon.png")
                    em.set_footer(text=self.bot.user.name, icon_url=self.bot.icon)
                    await message.channel.send(embed=em)