import discord
from discord.ext import commands
import yt_dlp
import asyncio
import uuid
import aiofiles.os

def download_video(url, output_path: str):
    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "allowed_extractors": ["youtube"],
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path

async def convert_to_gif(input_video, output_gif: str, start=0, duration=5):
    cmd = [
        "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", input_video,
        "-vf", "fps=10,scale=480:-1:flags=lanczos",
        output_gif
    ]

    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    return output_gif


class PremiumCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ytgif")
    @commands.cooldown(1, 60, type=commands.BucketType.guild)
    async def youtube_gif(self, ctx: commands.Context, url: str):
        v_file = uuid.uuid4()

        v_p = await asyncio.to_thread(download_video, url, f"temp/{v_file}.mp4")

        path = await convert_to_gif(v_p, f"temp/{v_file}.gif")

        try:

            file = discord.File(path, filename="gif.gif")
            await ctx.reply(file=file)
        except:
            await ctx.reply('https://tenor.com/view/cat-no-nonono-noooo-cat-no-gif-13597132752790194338')

        await asyncio.sleep(2)

        await aiofiles.os.remove(f'temp/{v_file}.mp4')
        await aiofiles.os.remove(f'temp/{v_file}.gif')


async def setup(bot: commands.Bot):
    await bot.add_cog(PremiumCog(bot))