import discord
from discord.ext import commands
import json, asyncio, requests
from collections import namedtuple

def noMD(str):
    return str.replace("*", "").replace("_", "").replace("@everyone", "Everyone").replace("@here", "Here").replace("://", ";//").replace("\n", "\\n")


def currcode(crypto):
    cryptoStr = crypto.upper()
    if cryptoStr == "BTC":
        return "Bitcoin"
    if cryptoStr == "ETH":
        return "Ethereum"
    if cryptoStr == "XMR":
        return "Monero"
    if cryptoStr == "LTC":
        return "Litecoin"
    if cryptoStr == "ETC":
        return "Ethereum Classic"
    if cryptoStr == "BCH":
        return "Bitcoin Cash"
    else:
        if cryptoStr == "DOGE":
            return "Dogecoin"
        return "the given cryptocurrency"

def currMark(fiat):
    if fiat == "USD":
        return "$"
    if fiat == "GBP":
        return "£"
    if fiat == "EUR":
        return "€"
    if fiat == "JPY":
        return "¥"
    else:
        return f"{fiat} "

def getCCValue(to, fro):
    markets = ["Kraken", "Bitfinex", "GDAX", "Bitstamp", "BTCE", "Cryptsy", "Cexio", "Gemini", "Quoine", "Qryptos", "Bitflyer"]
    ConversionResult = namedtuple("ConversionResult", ["price", "market"])
    for market in markets:
        try:
            price = requests.get(f"https://api.cryptowat.ch/markets/{market.lower()}/{fro}{to}/price").json()
            return ConversionResult(price["result"]["price"], market)
        except:
            continue

    return ConversionResult("", "")

def badCommandError(self, ctx, desc):
    signature = ctx.command.signature
    em = createTextEmbed("Help", f"{self.bot.command_prefix}{ctx.command.name} {signature}", self.bot.color)
    em.add_field(name="**Description**", value=(ctx.command.help), inline=False)
    em.set_footer(text=(self.bot.user.name), icon_url=(self.bot.icon))
    return em

def createTextEmbed(title, desc, color):
    em = discord.Embed(title=title, description=desc, color=color)
    return em

def setup(bot):
    bot.add_cog(CryptoCurrency(bot))

class CryptoCurrency(commands.Cog, name="CryptoCurrency"):
    """
    Cryptocurrency-related commands
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True, aliases=["crypto", "ltc", "eth", "cryptocoin", "cryptocurrency", "xmr", "etc", "bch"])
    async def btc(self, ctx, currency="USD", crypto="BTC"):
        """Get the current value of cryptocurrencies like Bitcoin"""
        async with ctx.channel.typing():
            currency = currency.lower()
            crypto = crypto.lower()
            if currency == "help":
                await ctx.channel.send(embed=(badCommandError(self, ctx, "")))
                return
            currencyMark = currMark(currency.upper())

            try:
                res = getCCValue(currency, crypto)
                price = res.price
                market = res.market
                if price == "" or market == "":
                    raise Exception("Price or market is NULL.")
                cryptoStr = currcode(crypto)
                em = discord.Embed(title=f"{cryptoStr} Value in {currency.upper()}", description=f"At {market}, {cryptoStr} is currently worth **{currencyMark}{price}**.",
                  color=0xfe9840)
                em.set_author(name=f"{cryptoStr} Value", icon_url="https://shuga.co/assets/donate/btc.png")
                em.set_footer(text=self.bot.user.name, icon_url=(self.bot.icon))
                await ctx.channel.send(embed=em)
            except:
                em = discord.Embed(title="Error", description=f"The currency exchange\
                    ({noMD(currency.upper())} -> {noMD(crypto.upper())}) is invalid.\
                    Try another traditional (such as USD or GBP) or crypto (such as BTC or ETH) currency.",
                  color=0xfe9840)
                em.set_author(name="Cryptocurrency Value", icon_url="https://shuga.co/assets/donate/btc.png")
                em.set_footer(text=(self.bot.user.name), icon_url=(self.bot.icon))
                await ctx.channel.send(embed=em)