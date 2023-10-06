# @xditya

import logging

import discord
from discord.ext import commands
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("task-1")

try:
    BOT_TOKEN = config("BOT_TOKEN")
except Exception as e:
    log.error(f"Error loading environment variables: {e}")
    exit(1)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!", intents=intents, description="This is a test bot"
)


@bot.event
async def on_ready():
    print("Bot is running!")


@bot.event
async def on_member_join(member):
    if member.bot or not member.guild.system_channel:
        return
    try:
        # dm the member
        await member.create_dm()
        await member.dm_channel.send(
            f"Hi {member.mention}, welcome to {member.guild.name}. Hope you enjoy your stay!"
        )

        # send a welcome message to the welcome channel
        # this sends welcome to the channel named "welcomes" in the server
        channel = discord.utils.get(member.guild.channels, name="welcomes")
        await channel.send(f"Welcome {member.mention} to {member.guild.name}!")
    except Exception as e:
        log.error(f"Error sending welcome message to {member.name}: {e}")


@bot.command("start", help="Starts the bot")
async def ping(ctx):
    await ctx.send(
        "Hello there!\n\nView source: https://github.com/xditya/mulearn-discord-tasks"
    )


bot.run(BOT_TOKEN)
