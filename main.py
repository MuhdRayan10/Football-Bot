import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix='+')

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')


@client.command()
async def sync(ctx):
    fmt = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(fmt)} commands")


@client.event
async def on_ready():
    await load_cogs()
    print(f"Connected to discord as {client.user}")
    await client.change_presence(activity=discord.Game(name="Footballing..."))
    await sync()
    
load_dotenv()
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)