from discord.embeds import Embed
from discord.colour import Color
from discord.ext import commands
from ossapi import Ossapi
from ossapi import enums
from ossapi import models

import pickle
import os
import logger
import discord

BASE_URL = "https://osu.ppy.sh/"
ICON_URL = "https://flagcdn.com/w80/%s.png"

class User:
    def __init__(self, user: models.User) -> None:
        self.username = user.username
        self.id = user.id
        self.avatar_url = user.avatar_url
        self.global_rank = user.statistics.global_rank
        self.country_code = user.country_code
        self.country_rank = user.statistics.country_rank
        self.peak_rank = user.rank_highest.rank
        self.peak_rank_update = int(user.rank_highest.updated_at.timestamp())
        self.level_current = user.statistics.level.current
        self.level_progress = round(user.statistics.level.progress, 2)
        self.pp = user.statistics.pp
        self.accuracy = round(user.statistics.hit_accuracy, 2)
        self.play_count = user.statistics.play_count
        self.play_time = int(user.statistics.play_time/3600)
        if user.last_visit != None:
            self.last_seen = f"Last seen {user.last_visit.strftime('%d-%m-%Y %H:%M:%S')} UTC on Bancho"
        else:
            self.last_seen = "User is online on Bancho"

class osuApi(commands.Cog):
    def __init__(self, bot, config) -> None:
        self.bot = bot
        self._id = config["client_id"]
        self._secret = config["client_secret"]
        self.uri = config["redirect_uri"]
        if not os.path.exists('./cogs/osu'):
            os.mkdir('./cogs/osu')
        if (self.uri != ""):
            self.api = Ossapi(self._id, self._secret)
        else:
            self.api = Ossapi(self._id, self._secret, self.uri)
        self.gameModes = [e.value for e in enums.GameMode]

    @commands.command(name="link", help="Link your osu account")
    async def link(self, ctx: discord.Interaction, username=None, mode=None):
        if (username == None):
            await ctx.channel.send("Please enter your username!")
            return
        
        if (mode not in self.gameModes):
            mode = "osu"

        try:
            _ = self.api.user(username, mode=mode)
        except ValueError:
            embed = Embed(title="\u200b",color=Color.from_rgb(255, 0, 0))
            embed.add_field(value=f"**User {username} is not exist!**")
            return await ctx.channel.send(embed=embed)
        
        with open('./cogs/osu/' + str(ctx.message.author.id), 'wb') as f:
            pickle.dump(username, f)

        embed = Embed(title="\u200b",color=Color.from_rgb(255, 0, 0))
        embed.add_field(name="\u200b", value=f"Your account is now **{username}**")
        return await ctx.channel.send(embed=embed)

    @commands.command(name="osu", aliases=["o"], help="Show your osu account")
    async def get_user(self, ctx: discord.Interaction, username=None, mode=None):
        if (username == None):
            try:
                username = pickle.load(open('./cogs/osu/' + str(ctx.message.author.id), 'rb'))
            except FileNotFoundError:
                username = ctx.message.author.name

        if (mode not in self.gameModes):
            mode = "osu"
            
        user = None
        try:
            user = User(self.api.user(username, mode=mode))
        except ValueError:
            embed = Embed(title=" ",color=Color.from_rgb(108,250,243))
            embed.add_field(name="", value=f"**User: {username} is not exist!**")
            return await ctx.channel.send(embed=embed)

        embedData = (f"▸ **Bancho Rank**: #{user.global_rank:2,} ({user.country_code}#{user.country_rank:2,})\n"+
                    f"▸ **Peak Rank**: #{user.peak_rank:,} achieved <t:{user.peak_rank_update}:R>\n"+
                    f"▸ **Level**: {user.level_current} + {user.level_progress}%\n"+
                    f"▸ **PP**: {user.pp:,} **Acc**: {user.accuracy}%\n"+
                    f"▸ **Playcount**: {user.play_count:,} ({user.play_time} hrs)")
        
        embed = Embed(title=" ", color=Color.from_rgb(108,250,243))
        embed.set_author(name=f"osu! Profile for {user.username}",
                        url=(BASE_URL + 'u/' + str(user.id)),
                        icon_url=(ICON_URL % user.country_code.lower()))
        embed.add_field(name="", value=embedData, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=user.last_seen, icon_url=ctx.message.author.avatar)

        await ctx.channel.send(embed=embed)
        return
    
    @commands.command(name="country", aliases=["cr"], help="Show country ranking lb (vn only)")
    async def get_cr_lb(self, ctx: discord.Interaction, beatmap: str):
        mapID = beatmap.split("/")[-1]
        data = self.api.beatmap_scores(int(mapID), type="country")
        logger.info("get_cr_lb", "abc")
        logger.info("get_cr_lb", data)
