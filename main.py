import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='+')

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


@bot.command()
async def sync():
    fmt = await bot.tree.sync()
    print(f"{fmt} commands have been synced")


@bot.event
async def on_ready():
    await load_cogs()
    print(f"Connected to discord as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Footballing..."))
    await sync()
    
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)