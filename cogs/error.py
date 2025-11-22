import traceback
from discord.ext import commands
import discord

class ErrorHandleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        # error_details = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        if isinstance(error, commands.CommandNotFound):
            a = None
            return a
        elif isinstance(error, commands.NotOwner):
            return await ctx.reply("https://tenor.com/view/cat-no-nonono-noooo-cat-no-gif-13597132752790194338")
        elif isinstance(error, commands.CommandOnCooldown):
            a = None
            return a
        elif isinstance(error, commands.NoPrivateMessage):
            a = None
            return a
        elif isinstance(error, commands.BadArgument):
            return await ctx.reply("https://tenor.com/view/cat-no-nonono-noooo-cat-no-gif-13597132752790194338")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply("https://tenor.com/view/cat-no-nonono-noooo-cat-no-gif-13597132752790194338")
        else:
            print(f"Prefix Command error: {error}")
            return await ctx.reply("https://tenor.com/view/error-gif-26155260")

async def setup(bot):
    await bot.add_cog(ErrorHandleCog(bot))