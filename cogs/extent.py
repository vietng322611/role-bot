from discord import app_commands
from discord.ext import commands

import discord
import requests
import logger
import csv

class extent(commands.Cog):
    def __init__(self, bot: commands.Bot, config):
        self.bot = bot
        self.config = config

    @app_commands.command(name="role-create", description="Create roles from csv")
    async def role_create(
        self,
        ctx: discord.Interaction,
        csv_file: discord.Attachment
    ):
        try:
            file = requests.get(csv_file.url)
            content = list(csv.reader(file.content.decode('utf-8-sig').splitlines()))

            guild = ctx.guild
            guild_roles = [str(x) for x in guild.roles]
            filtered_roles = list(filter(lambda x: x not in guild_roles, content[0]))
            count = 0
            for role in filtered_roles:
                try:
                    await guild.create_role(name=role)
                    count += 1
                except Exception as e:
                    logger.error("role_create", str(e))

            await ctx.response.send_message(f"Created {count} roles.")
        except Exception as e:
            logger.error("role_create", str(e))

    @app_commands.command(name="role-add", description="Add roles from csv")
    async def role_add(
        self,
        ctx: discord.Interaction,
        csv_file: discord.Attachment
    ):
        try:
            file = requests.get(csv_file.url)
            content = list(csv.reader(file.content.decode('utf-8-sig').splitlines()))
            guild_roles = [str(x) for x in ctx.guild.roles]
            
            guild = ctx.guild
            total_member_added = 0
            for row in content:
                role = row[0]
                if role not in guild_roles:
                    await guild.create_role(name=role)

                members = row[1:]
                filtered_members = list(filter(lambda x: str(x) in members, guild.members))
                for member in filtered_members:
                    try:
                        await member.add_roles(role)
                        total_member_added += 1
                    except Exception as e:
                        logger.error("role_add", str(e))

            await ctx.response.send_message(f"Added {len(content)} roles to {total_member_added} members.")
        except Exception as e:
            logger.error("role_add", str(e))

    @app_commands.command(name="role-remove", description="Remove member's roles from csv")
    async def role_remove(
        self,
        ctx: discord.Interaction,
        csv_file: discord.Attachment
    ):
        try:
            file = requests.get(csv_file.url)
            content = list(csv.reader(file.content.decode('utf-8-sig').splitlines()))

            members = [x[0] for x in content[1:]]
            guild = ctx.guild
            filtered_roles = list(filter(lambda x: str(x) in content[0], guild.roles))
            filtered_members = list(filter(lambda x: str(x) in members, guild.members))
            failed = 0
            for member in filtered_members:
                try:
                    await member.remove_roles(*filtered_roles)
                except Exception as e:
                    failed += 1
                    logger.error("role_remove", str(e))

            await ctx.response.send_message(f"Removed {len(filtered_roles)} roles from {len(filtered_members) - failed} members.")
        except Exception as e:
            logger.error("role_remove", str(e))

    @app_commands.command(name="role-delete", description="Delete roles from csv")
    async def role_delete(
        self,
        ctx: discord.Interaction,
        csv_file: discord.Attachment
    ):
        try:
            file = requests.get(csv_file.url)
            content = list(csv.reader(file.content.decode('utf-8-sig').splitlines()))

            guild = ctx.guild
            filtered_roles = list(filter(lambda x: str(x) in content[0], guild.roles))
            count = 0
            for role in filtered_roles:
                try:
                    await guild._remove_role(name=role.id)
                    count += 1
                except Exception as e:
                    logger.error("role_delete", str(e))

            await ctx.response.send_message(f"Deleted {count} roles.")
        except Exception as e:
            logger.error("role_delete", str(e))

    @app_commands.command(name="close", description="Close the bot")
    async def close(self, ctx: discord.Interaction):
        if ctx.message.author.id == self.config["creator_id"]:
            await ctx.response.send_message("Bot terminated!")
            await self.bot.close()
        else:
            ctx.response.send_message("You can't use this command!")