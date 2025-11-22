import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog_name: str):
        await self.bot.reload_extension(f"cogs.{cog_name}")
        await ctx.reply("https://tenor.com/view/cocking-pistol-john-wick-keanu-reeves-john-wick-chapter-4-jw4-gif-14490794064585307818")

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))