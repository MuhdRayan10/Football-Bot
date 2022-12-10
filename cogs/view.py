from discord.ext import commands
from Backend.cards import create_card, create_team, create_team_image
from discord import app_commands
import discord

from io import BytesIO
import discord

class View(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='view', description="View Images of players, teams, etc")
    @app_commands.describe(field="The type of image you want to view")
    @app_commands.choices(field=[
        app_commands.Choice(name="Player", value="player"),
        app_commands.Choice(name="Squad", value="squad"),
        app_commands.Choice(name="Starting XI", value="11")])
    async def view(self, interaction:discord.Interaction, field:str, name:str):
        
        user = interaction.user
        if field == "player":
            with BytesIO() as image_binary:
                card = create_card(user.id, name)
                if not card: 
                    await interaction.response.send_message(f"I couldn't find a player with the name `{name}`... Please try again!")
                    return
                card.save(image_binary, 'PNG')
                image_binary.seek(0)
                await interaction.response.send_message(file=discord.File(fp=image_binary, filename='image.png'))
        elif field == 'squad':
            team = create_team(user.id, name)
            
            if not team:
                await interaction.response.send_message(f"A team with the name `{name}` was not found...")
                return
            
            n = 1989
            final_list = ['']
            for sentence in team:
                if len(final_list[-1] + sentence) <= n:
                    final_list[-1] += sentence + '\n'
                else:
                    final_list.append(sentence)


            for i, msg in enumerate([f"```css\n{i}```" for i in final_list]):
                if not i: await interaction.response.send_message(msg)
                else:
                    await interaction.followup.send(msg)
                    

        elif field == '11':
            with BytesIO() as image_binary:
                team = create_team_image(name, user.id)
                if not team:
                    await interaction.response.send_message(f"A team with the name `{name}` was not found...")
                    return

                team.save(image_binary, 'PNG')
                image_binary.seek(0)
                await interaction.response.send_message(file=discord.File(fp=image_binary, filename='image.png'))    

        else:
            await interaction.response.send_message(f"Could not recognize the field `{field}`")



async def setup(client):
    await client.add_cog(View(client))