from Backend.generator import generate_world, destroy_world
from discord.ext import commands
from discord import app_commands
from easy_sqlite3 import *
import asyncio
import discord


class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

        db = Database('./Data/users.db')
        db.create_table('users', {'id':INT, 'name':TEXT})

        db.close()

    @app_commands.command(name="register", description="Create your own football world!")
    async def register(self, interaction:discord.Interaction, name: str):
        
        db = Database('./Data/users.db')

        if not db.if_exists('users', {'id':interaction.user.id}):
            
            db.insert('users', (interaction.user.id, name))

            await interaction.response.send_message(f"Registered {interaction.user.mention} as `{name}`!") 
            generate_world(interaction.user.id)

            db.close()
        else:    
            await interaction.response.send_message("Looks like you have already registered!")
    
    @app_commands.command(name="unregister", description="Delete your world")
    async def unregister(self, interaction:discord.Interaction):
        db = Database('./Data/users.db')
        user = interaction.user
    
        if db.if_exists('users', {'id':user.id}):
            db.delete('users', where={'id':user.id})

            await interaction.response.send_message(f"Unregistered {user.mention}... Sad to see you go :(")
            destroy_world(user.id)
        else:
            await interaction.response.send_message("Looks like you aren't even registered to begin with.")

        db.close()

async def setup(client):
    await client.add_cog(Register(client))