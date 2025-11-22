import time
import discord
from discord.ext import commands
import aiohttp
import datetime

cooldown_afk = {}

class HelloCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command(name="hello")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def hello(self, ctx: commands.Context):
        url = await self.bot.get_gif("hello")
        await ctx.reply(url)

    @commands.command(name="good")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def good(self, ctx: commands.Context):
        url = await self.bot.get_gif("good")
        await ctx.reply(url)

    @commands.command(name="get", aliases=["search"])
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def get(self, ctx: commands.Context, *, gif_name: str):
        url = await self.bot.get_gif(gif_name)
        await ctx.reply(url)

    @commands.command(name="help")
    @commands.cooldown(2, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def help(self, ctx: commands.Context):
        await ctx.reply('''
> ❔help
> 👍hello, good, 123
> 🔍get, search, weather
> 🧰afk, now
> 🔨kick, ban
> 🚫reload
''')

    @commands.command(name="123")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def _123(self, ctx: commands.Context):
        url = await self.bot.get_gif("123")
        await ctx.reply(url)

    @commands.command(name="kick")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def _kick(self, ctx: commands.Context, member: discord.Member):
        await member.kick()
        url = await self.bot.get_gif("kick")
        await ctx.reply(url)

    @commands.command(name="ban")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def _ban(self, ctx: commands.Context, user: discord.User):
        await ctx.guild.ban(user)
        url = await self.bot.get_gif("ban")
        await ctx.reply(url)

    @commands.command(name="weather")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def weather(self, ctx: commands.Context):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                ts = data[0]["timeSeries"][0]
                time_defs = ts["timeDefines"]
                area = ts["areas"][0]
                weathers = area["weathers"]

                weather_info = []
                for dt, w in zip(time_defs, weathers):
                    weather_info.append((dt, w))

                for dt, w in weather_info:
                    if not isinstance(w, str):
                        return
                    if w.startswith('晴れ'):
                        url = await self.bot.get_gif("晴れ")
                        return await ctx.reply(content=url)
                    elif w.startswith('くもり'):
                        url = await self.bot.get_gif("くもり")
                        return await ctx.reply(content=url)
                    else:
                        url = await self.bot.get_gif("分からない")
                        return await ctx.reply(content=url)

    @commands.command(name="now")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def now(self, ctx: commands.Context):
        t = datetime.datetime.now().strftime('%H時')
        url = await self.bot.get_gif(t)
        await ctx.reply(url)

    @commands.command(name="afk")
    @commands.cooldown(1, 5, type=commands.BucketType.guild)
    @commands.guild_only()
    async def afk(self, ctx: commands.Context, *, 理由: str):
        self.afk_users[str(ctx.author.id)] = 理由
        url = await self.bot.get_gif("ok")
        await ctx.reply(url)

    @commands.Cog.listener("on_message")
    async def on_message_afk(self, message: discord.Message):
        if message.author.bot:
            return
        
        if not message.content.startswith('gif '):
            if str(message.author.id) in self.afk_users:
                reason = self.afk_users[str(message.author.id)]
                del self.afk_users[str(message.author.id)]
                url = await self.bot.get_gif("おかえりなさい")
                await message.reply(url)
                await message.channel.send(embed=discord.Embed(title="放置理由", description=reason, color=discord.Color.blue()))
                return
            
        mentions = message.mentions
        if mentions == []:
            return
        for k, v in self.afk_users.items():
            if str(mentions[0].id) == k:

                # クールダウンをチェック
                current_time = time.time()
                last_message_time = cooldown_afk.get(message.guild.id, 0)
                if current_time - last_message_time < 3:
                    return
                cooldown_afk[message.guild.id] = current_time

                await message.reply('https://tenor.com/view/afk-brb-afk-brb-gif-2441409518889357786')
                return

async def setup(bot: commands.Bot):
    await bot.add_cog(HelloCog(bot))