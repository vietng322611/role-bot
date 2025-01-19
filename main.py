# This made by vietng322611, please be respect, don't copy it without permission, you can change the code inside into your own.
# If something goes wrong, DM me your log or try restarting the bot.

import modwall; modwall.check() # Library check

from generate_config import gen; gen()

from discord.ext import commands
from dotenv import load_dotenv
from cogs.extent import extent
from cogs.osuApi import osuApi

import asyncio
import os
import json
import discord
import logger
import sys

config = json.load(open('./config.json'))

if not os.path.exists(config['log_path']):
    os.mkdir(config['log_path'])

logger.config(config["log_path"])
sys.excepthook = logger.excepthook

load_dotenv('token.env')
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.all()
bot = commands.Bot(description="Create roles and give roles from csv", command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    logger.info('on_ready', f'Connected!')

async def main():
    async with bot:
        await bot.add_cog(extent(bot, config))
        # await bot.add_cog(osuApi(bot, config))
        await bot.start(TOKEN)

if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('main', "ctrl+C captured!")
    finally:
        logger.info('main', "Bot closed!")