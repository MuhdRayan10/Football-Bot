from discord.ext import commands
from easy_sqlite3 import *
import os

OWNERS = [984245773887766551]

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reset(self, ctx):
        if ctx.author.id not in OWNERS:
            await ctx.reply("You do not have permission to reset all data")
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

        await ctx.reply("Deleted: {}".format('\n'.join([u[1] for u in users])))

        
async def setup(client):
    await client.add_cog(Owner(client))
