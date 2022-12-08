from discord import app_commands
from discord.ext import commands
from easy_sqlite3 import *
from discord.ui import View
import discord, asyncio


def add_mail(user_id, msg, subject, sender, type_):
    mail_db = Database(f"./Data/Worlds/{user_id}/mail")

    mail_db.insert("inbox", (msg, subject, sender, type_, 0))
    mail_db.close()

class OfferView(View):
    def __init__(self, mail, name, user_id, msg):
        self.mail = mail
        self.name = name
        self.user_id = user_id

        self.read = False
        self.msg = msg

        self.time = 20

        super().__init__(timeout=self.time)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_offer(self, interaction, _):
        self.read = True
        await interaction.response.defer()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_offer(self, interaction, _):
        self.read = True
        await interaction.response.defer()

    @discord.ui.button(label="Stall", style=discord.ButtonStyle.grey)
    async def stall_offer(self, interaction, _):
        self.read = True
        await interaction.respons.defer()

    async def on_timeout(self) -> None:
        for btn in self.children:
            btn.disabled = True

        await self.msg.edit(view=self)
    
    async def if_msg_read(self):
        count = 0
        while not self.read and count < self.time*2:
            count += 1
            await asyncio.sleep(0.5)

        if self.read:
            return True

class MessageView(View):
    def __init__(self, mail, name, user_id, msg):
        self.mail = mail
        self.name = name
        self.user_id = user_id

        self.msg = msg

        self.time = 20
        super().__init__(timeout=self.time)

        self.read = False

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def mark_msg_read(self, interaction, _):
        pass

        mail_db = Database(f"./Data/Worlds/{self.user_id}/mail")

        mail_db.update("inbox", {'status':1}, where={'subject':self.mail['subject'], 'message':self.mail['message'], 'sender':self.mail['sender'], 'type':self.mail['type']})
        mail_db.close()

        await interaction.response.defer()

        self.read = True

    async def on_timeout(self) -> None:
        self.children[0].disabled = True

        await self.msg.edit(view=self)
        

    async def if_msg_read(self):
        count = 0
        while not self.read and count < self.time*2:
            count += 1
            await asyncio.sleep(0.5)

        if self.read:
            return True

class Mail(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.unread_mails = {}


    async def display_mails(self, user_id, name, msg=None, ctx=None):

        if self.unread_mails[user_id] != 'done' or not len(self.unread_mails[user_id]):
    
            mail = self.unread_mails[user_id].pop()

            embed= discord.Embed(title=mail['subject'], description=mail['sender'], color=0xef2525)
            embed.set_author(name="INBOX")
            embed.add_field(name=f"Respected {name},", value=mail['message'], inline=True)
            embed.set_footer(text="Made with love · Rayan10#5701")
            
            view = OfferView(mail, name, user_id, msg) if mail['type'] == 'offer' else MessageView(mail, name, user_id, msg)            
            if msg:
                await view.msg.edit(embed=embed, view=view)
            else:
                view.msg = await ctx.response.send_message(embed=embed, view=view)

            result = await view.if_msg_read()
            if not result: return

            if len(self.unread_mails[user_id]):
                await self.display_mails(user_id, name, view.msg)
            else:
                await view.msg.edit(embed=discord.Embed(title="All Mails Read", color=0x2ecc71), view=None)

        else:
            await msg.edit(embed=discord.Embed(title="All Mails Read", color=0x2ecc71), view=None)

    @app_commands.command(name="mail", description="View your world's notifications")
    async def mail(self, interaction: discord.Interaction):
        user = interaction.user.id
        mail_db = Database(f"./Data/Worlds/{user}/mail")
        user_db = Database(f"./Data/users")


        if mail_db.if_exists("inbox", where={"status": 0}):

            mails = mail_db.select("inbox", where={"status":0}, dict_format=True)
            name = user_db.select("users", selected=["name"], size=1, where={"id": user})[0]

            self.unread_mails[user] = [mails] if isinstance(mails, dict) else mails

            mail_db.close()
            user_db.close()
            
            await self.display_mails(user, name, ctx=interaction)

        else:
            await interaction.response.send_message("No new messages!")
            

                 
async def setup(client):
    await client.add_cog(Mail(client))
