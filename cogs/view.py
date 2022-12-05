from discord.ext import commands
from Backend.cards import create_card, create_team

from io import BytesIO
import discord

class View(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['view', 'inspect'])
    async def show(self, ctx, field, *data):
        if field in ('player'):
            name = ' '.join(data)
            with BytesIO() as image_binary:
                card = create_card(ctx.author.id, name)
                if not card: 
                    await ctx.reply(f"I couldn't find a player with the name `{name}`... Please try again!")
                    return
                card.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        elif field in ('team'):
            team = create_team(ctx.author.id, ' '.join(data))
            if not team:
                await ctx.reply(f"A team with the name `{team}` was not found...")
                return

            n = 2000
            final_list = ['']
            for sentence in team:
                if len(final_list[-1] + sentence) <= n:
                    final_list[-1] += sentence + '\n'
                else:
                    final_list.append(sentence)

            for msg in final_list:
                await ctx.send(msg)

        else:
            await ctx.reply(f"Could not recognize the field `{field}`")



async def setup(client):
    await client.add_cog(View(client))