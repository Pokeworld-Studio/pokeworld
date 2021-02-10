import discord
from discord import Intents

from discord.ext.commands.errors import (BadArgument, BotMissingPermissions, MissingRequiredArgument, MissingPermissions)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.errors import HTTPException

from ..db import db

PREFIX = "?"
OWNER_IDS = [549213551236087808, 602779813089902600]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )

    def setup(self):
        self.load_extension('lib.cogs.pokemon')

        print("Setup Complete.")

    def run(self, version):
        self.VERSION = version

        print("Running Setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connecting...")
       
    async def on_disconnect(self):
        print("Bot Disconnected.")
        
    async def on_error(self, err, *args, **kwargs):
        pass
        
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send(f"Invalid arguments, {ctx.author.mention}!")
        elif isinstance(exc, MissingPermissions):
            await ctx.send(f"Permission for you to execute that command is denied, {ctx.message.author.mention}!")
        elif isinstance(exc, BotMissingPermissions):
            await ctx.send(f"I'm missing the permissions to execute that task, {ctx.message.author.mention}!")
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(f"You're missing an argument, {ctx.author.mention}")
        elif isinstance(exc.original, HTTPException):
            await ctx.send(f"Unfortunately, I'm unable to respond, {ctx.message.author.mention}.")
        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.scheduler.start()

            countGuild = self.get_guild(808125504435257394)
            count = len(countGuild.members)

            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} members"))

            print("Bot Ready.")

        else:
            print("Bot Reconnected.")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()