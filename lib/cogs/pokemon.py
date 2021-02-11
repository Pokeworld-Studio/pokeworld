from discord.ext.commands import command
from discord.ext.commands import Cog

from discord import Embed, embeds

import discord
import asyncio

from ..db import db

class Pokemon(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x4287f5

    @command(name="serverinfo", aliases=["si"], brief="Displays Pokéworld's server info")
    async def show_server_stats(self, ctx):
        '''Displays Pokéworld's server info!'''
        embed = Embed(title="Server Info",
                      colour=0x4287f5)
        embed.add_field(name="Server Information", value=f"**Members:** {len(ctx.guild.members)}\n**Server ID:** {ctx.guild.id}\n**Server Region:** Europe\n**Server Timezone:** GMT\n**Total Text Channels:** {len(ctx.guild.text_channels)}\n**Total Voice Channels:** {len(ctx.guild.voice_channels)}", inline=False)
        embed.add_field(name="Other Information", value=f"**Total Roles:** {len(ctx.guild.roles)}\n**Total Emojis:** {len(ctx.guild.emojis)}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @command(name="vote", aliases=["v"], brief="Helps you vote for the server")
    async def vote_server(self, ctx):
        '''Helps you vote for the server'''
        embed = Embed(title="Help support this server!",
                      description="[Vote for Pokéworld on top.gg!](https://top.gg/servers/808125504435257394/vote)",
                      colour=0x4287f5)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        embed = message.embeds[0]
        if message.guild.id == 808125504435257394:
            if message.author.id == 716390085896962058:
                if "purchased" in message.content:
                    if "Incense" in message.content:
                        if "You" in message.content:
                            await message.channel.send("<@&809033944304451594> - Somone used an Incense!")
            
                else:
                    if "These" in message.content:
                        if "seems" in message.content:
                            db.execute("UPDATE server SET Shinies = Shinies + 1 WHERE GuildID = ?", 808125504435257394)

            elif "Bump" in embed.description:
                if "done" in embed.description:
                    if message.author.id == 302050872383242240: 
                        await asyncio.sleep(7200)
                        channel = self.bot.get_channel(808125504435257397)
                        await channel.send("It's been two hours since the last bump. What are you waiting for? Get over to <#808730678849568779> and type `!d bump`!")
                
            else:
                battles = ["P!DUEL", "P!BATTLE", "p!battle", "p!duel", "P!duel", "P!battle", "p!DUEL", "p!BATTLE", "p!Battle", "p!Duel"]
                for starter in battles:
                    if message.content.startswith(f"{starter}"):
                        db.execute("UPDATE server SET Battles = Battles + 1 WHERE GuildID = ?", 808125504435257394)
            
    @Cog.listener()
    async def on_ready(self):
        print("Cog Ready: 'Pokemon'")

def setup(bot):
    bot.add_cog(Pokemon(bot))