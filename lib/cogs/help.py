from discord.ext.commands import command
from discord.ext.commands import Cog

from discord import Embed
from discord.utils import get

from typing import Optional

import discord
import asyncio

from ..db import db

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []
    
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"`{cmd_and_aliases} {params}`"

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0x4287f5
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help - `?{command}`",
                      description=syntax(command),
                      colour=self.colour)
        embed.add_field(name="Command Description", value=command.help)
        self.cmd_help_desc = command.help
        await ctx.send(embed=embed)

    @command(name="help", brief="Shows this message.")
    async def show_help(self, ctx, cmd: Optional[str]):
        '''Shows this message.'''
        if cmd is None:
            embed = Embed(colour=0x4287f5)
            string = ""
            for cmd_name in self.bot.commands:
                cmd_and_aliases = "|".join([str(cmd_name), *cmd_name.aliases])
                string += f"`{cmd_and_aliases}`" + "\n"
            embed.add_field(name=f"**Bot Commands**", value=f"{string}\nIf you need more info on a command,\ntype `?help <command>`", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That isn't a valid command.")

    @command(name="invite", aliases=["inv"], brief="Provides an invite link for this server")
    async def give_invite(self, ctx):
        '''Provides an invite link for this server'''
        await ctx.send("You can use this link to allow people to invite people to the server:\nhttps://discord.gg/KwnCufrDDm")

    @command(name="advertise", aliases=["advert", "ad"], brief="Provides a message to advertise Pokéworld")
    async def advertise_sever(self, ctx):
        '''Provides a message to advertise Pokéworld'''
        ad = "```**Welcome to Pokéworld, a friendly Pokétwo community!\n**Right now you are looking at Pokéworld, the friendly Pokétwo community\nwhere you can discuss your favourite thing in the world - Pokémon!\n\n**Rules & Guidelines:**\nTo make Pokéworld the friendly, safe community we all strive for it to be,\nwe'll need *you* to help out by abiding by these rules!\n\n- Do not spam invites, links, messages, mentions, etc.\n- Do not try to avoid mutes; your punishment will only get worse\n- Do not send any NSFW images, files, or content whatsoever\n- Do not disrespect staff; they are there to help you\n- Do not say something that you know may incite an argument\n\n**However, please note that:**\n> If you don't feel comfortable with any of these rules, you may open a modmail ticket\n> and a member of staff will be with you shortly```"
        embed = Embed(title="Advetisement!", 
                      description=f"You can use this link to advertise **Pokéworld**! All you need to do is copy and paste the following into a server advertising channel in another server!\n{ad}",
                      colour=self.colour)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        print("Cog Ready: 'Help'")

def setup(bot):
    bot.add_cog(Help(bot))