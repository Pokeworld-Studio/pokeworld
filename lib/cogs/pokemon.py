from re import T
from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import Embed

import discord

from ..db import db

class Pokemon(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x4287f5

    @command(name="serverinfo", aliases=["si"])
    async def show_server_stats(self, ctx):
        battles = db.field("SELECT Battles FROM server WHERE GuildID = 808125504435257394")
        trades = db.field("SELECT Trades FROM server WHERE GuildID = 808125504435257394")
        embed = Embed(title="Server Info",
                      description=f"**Battles:** {battles}\n**Trades:** {trades}\n**Members:** {len(ctx.guild.members)}\n",
                      colour=0x4287f5)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 808125504435257394:
            if message.author.id == 716390085896962058:
                if "purchased" in message.content:
                    if "Incense" in message.content:
                        if "You" in message.content:
                            await message.channel.send("<@&809033944304451594> - Somone used an Incense!")
            else:
                battles = ["P!DUEL", "P!BATTLE", "p!battle", "p!duel", "P!duel", "P!battle", "p!DUEL", "p!BATTLE"]
                for starter in battles:
                    if message.content.startswith(f"{starter}"):
                        db.execute("UPDATE server SET Battles = Battles + 1 WHERE GuildID = ?", 808125504435257394)
                trades = ["p!t", "p!trade"]
                for start in trades:
                    if message.content.startswith(f"{start}"):
                        db.execute("UPDATE server SET Trades = Trades + 1 WHERE GuildID = ?", 808125504435257394)

    @Cog.listener()
    async def on_ready(self):
        print("Cog Ready: 'Pokemon'")

def setup(bot):
    bot.add_cog(Pokemon(bot))