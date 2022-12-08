from discord.ext import commands
from discord import app_commands
from easy_sqlite3 import *
import discord
import os

OWNERS = [984245773887766551]

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='reset', description='Delete all user worlds from the database')
    async def reset(self, interaction: discord.Interaction):
        if interaction.user.id not in OWNERS:
            await interaction.response.send_message("You do not have permission to reset all data")
            return
        
        from shutil import rmtree

        db = Database("./Data/users")
        users = db.select('users')

        for user in users:
            try:
                rmtree(f"{os.getcwd()}\\Data\\Worlds\\{user[0]}")
            except:
                pass
        db.delete('users')
        db.close()

        await interaction.response.send_message("Deleted: {}".format('\n'.join([u[1] for u in users])))

        
async def setup(client):
    await client.add_cog(Owner(client), guilds=[discord.Object(id=1011656058277732412)])
