import discord
from discord.ext import commands
import dotenv
import os
import aiohttp
from urllib.parse import quote

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class GIFBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="gif ", help_command=None, intents=intents)

    async def setup_hook(self):
        await self.load_extension('cogs.hello')
        await self.load_extension('cogs.error')
        await self.load_extension('cogs.admin')
        await self.load_extension('cogs.premium')

    async def get_gif(self, word: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://g.tenor.com/v2/search?q={quote(word)}&key={os.environ.get("TENOR_API")}&limit=1&media_filter=minimal') as resp:
                try:
                    js = await resp.json()
                    gif_url = js.get('results', [])[0].get('media_formats', {}).get('gif', {}).get('url', None)
                    return gif_url
                except:
                    return None

bot = GIFBot()

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.CustomActivity(
            name=f"gif help | GIFだけで返します。"
        )
    )

bot.run(os.environ.get('TOKEN'))