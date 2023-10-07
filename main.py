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
intents.message_content = True

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


@bot.event
async def on_message(message):
    types = ["channel", "role"]
    actions = ["create", "edit", "delete"]
    # listen on "webhooks" channel
    if message.webhook_id and message.channel.name == "webhooks":
        try:
            content = eval(message.content)
        except Exception as e:
            log.error(f"Error parsing webhook message: {e}")
            return
        if (
            content.get("type") not in types
            or content.get("action") not in actions
            or not content.get("name")
        ):
            return await message.channel.send(
                "Invalid request recieved on webhook. Please check the format and try again."
            )
        name = content.get("name")
        guild = message.guild
        if content.get("type") == "channel":
            action = content.get("action")
            if action == "create":
                # create channel
                try:
                    all_channels = [c.name for c in guild.channels]
                    if name in all_channels:
                        return await message.channel.send(
                            "Channel with this name already exists. Please choose a different name."
                        )
                    await guild.create_text_channel(name)
                    await message.channel.send(f"Channel {name} created successfully!")
                except Exception as e:
                    log.error(f"Error creating channel {name}: {e}")
                    return await message.channel.send(
                        "Error creating channel. Please check the logs."
                    )
            elif action == "edit":
                # edit channel
                new_name = content.get("new_name")
                if not new_name:
                    return await message.channel.send(
                        "Invalid request recieved on webhook. Please check the format and try again."
                    )
                try:
                    all_channels = [c.name for c in guild.channels]
                    if name not in all_channels:
                        return await message.channel.send(
                            "Channel not found. Please check the name and try again."
                        )
                    if new_name in all_channels:
                        return await message.channel.send(
                            "Channel with this name already exists. Please choose a different name."
                        )
                    channel = discord.utils.get(guild.channels, name=name)
                    if channel is None:
                        return await message.channel.send(
                            "Channel not found. Please check the name and try again."
                        )
                    await channel.edit(name=new_name)
                    await message.channel.send(
                        f"Channel {name} renamed to {new_name} successfully!"
                    )
                except Exception as e:
                    log.error(f"Error editing channel {name}: {e}")
                    return await message.channel.send(
                        "Error editing channel. Please check the logs."
                    )
            elif action == "delete":
                # delete channel
                try:
                    channel = discord.utils.get(guild.channels, name=name)
                    if channel is None:
                        return await message.channel.send(
                            "Channel not found. Please check the name and try again."
                        )
                    await channel.delete()
                    await message.channel.send(f"Channel {name} deleted successfully!")
                except Exception as e:
                    log.error(f"Error deleting channel {name}: {e}")
                    return await message.channel.send(
                        "Error deleting channel. Please check the logs."
                    )
            return
        elif content.get("type") == "role":
            action = content.get("action")
            if action == "create":
                # create role
                try:
                    roles = [r.name for r in guild.roles]
                    if name in roles:
                        return await message.channel.send(
                            "Role with this name already exists. Please choose a different name."
                        )
                    await guild.create_role(name=name)
                    await message.channel.send(f"Role {name} created successfully!")
                except Exception as e:
                    log.error(f"Error creating role {name}: {e}")
                    return await message.channel.send(
                        "Error creating role. Please check the logs."
                    )
            elif action == "edit":
                # edit role
                new_name = content.get("new_name")
                if not new_name:
                    return await message.channel.send(
                        "Invalid request recieved on webhook. Please check the format and try again."
                    )
                try:
                    all_roles = [r.name for r in guild.roles]
                    if name not in all_roles:
                        return await message.channel.send(
                            "Role not found. Please check the name and try again."
                        )
                    if new_name in all_roles:
                        return await message.channel.send(
                            "Role with this name already exists. Please choose a different name."
                        )
                    role = discord.utils.get(guild.roles, name=name)
                    if role is None:
                        return await message.channel.send(
                            "Role not found. Please check the name and try again."
                        )
                    await role.edit(name=new_name)
                    await message.channel.send(
                        f"Role {name} renamed to {new_name} successfully!"
                    )
                except Exception as e:
                    log.error(f"Error editing role {name}: {e}")
                    return await message.channel.send(
                        "Error editing role. Please check the logs."
                    )
            elif action == "delete":
                # delete role
                try:
                    role = discord.utils.get(guild.roles, name=name)
                    if role is None:
                        return await message.channel.send(
                            "Role not found. Please check the name and try again."
                        )
                    await role.delete()
                    await message.channel.send(f"Role {name} deleted successfully!")
                except Exception as e:
                    log.error(f"Error deleting role {name}: {e}")
                    return await message.channel.send(
                        "Error deleting role. Please check the logs."
                    )
            return


@bot.command("start", help="Starts the bot")
async def ping(ctx):
    await ctx.send(
        "Hello there!\n\nView source: https://github.com/xditya/mulearn-discord-tasks"
    )


bot.run(BOT_TOKEN)
