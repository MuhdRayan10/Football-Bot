import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='+', application_id="1011612518160015380")

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')



@bot.event
async def on_ready():
    await load_cogs()
    print(f"Connected to discord as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Footballing..."))
    
async def main():

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    await bot.start(TOKEN)

asyncio.run(main())