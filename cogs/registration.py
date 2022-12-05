from Backend.generator import generate_world, destroy_world
from discord.ext import commands
from easy_sqlite3 import *
import asyncio


class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

        db = Database('./Data/users.db')
        db.create_table('users', {'id':INT, 'name':TEXT})

        db.close()

    @commands.command(aliases=['signup', 'new','start'])
    async def register(self, ctx):
        
        db = Database('./Data/users.db')

        if not db.if_exists('users', {'id':ctx.author.id}):
            await ctx.reply("What shall be your manager name?")
            try:
                name = await self.client.wait_for("message", check=lambda m: bool(len(m.content) and m.author.id == ctx.author.id), timeout=20.0)
            except asyncio.TimeoutError:
                await ctx.send("Looks like you don't want to register.")
                db.close()
                return
            
            db.insert('users', (ctx.author.id, name.content))
            
            await name.reply(f"Registered {ctx.author.mention} as `{name.content}`!")
            generate_world(ctx.author.id)

            db.close()
            return

        await ctx.reply("Looks like you have already registered!")
    
    @commands.command()
    async def unregister(self, ctx):
        db = Database('./Data/users.db')
        
        try:
            if db.if_exists('users', {'id':ctx.author.id}):
                db.delete('users', where={'id':ctx.author.id})

                await ctx.reply(f"Unregistered {ctx.author.mention}!")
                destroy_world(ctx.author.id)
            else:
                await ctx.reply("Looks like you aren't even registered to begin with.")
        except Exception as e:
            print(f"ERROR: {e}")

        db.close()

async def setup(client):
    await client.add_cog(Register(client))