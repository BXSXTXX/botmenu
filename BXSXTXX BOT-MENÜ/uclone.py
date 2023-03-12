import asyncio
import discord
import os
import requests
from discord.ext import commands


class uclone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gespeicherte_nutzer = {}


    @commands.command()
    async def clone(self, ctx, nutzer_id: int, zeit: int = None):
    """ 
    Anwendung: !clone [NutzerID] [Zeit in Minuten(optional)]
    Kopiert den mit der ID angegebenen Nutzer auf dein eigenes Profil xdd"""
        try:
            user = await self.bot.fetch_user(nutzer_id)
        except discord.NotFound:
            await ctx.send("Nutzer nicht gefunden.")
            return
        original_avatar = self.bot.user.avatar_url
        original_username = self.bot.user.name
        await self.bot.user.edit(avatar=user.avatar_url, username=user.name)
        if zeit is not None:
            # Warte die angegebene Zeit
            await asyncio.sleep(zeit * 60)
            await self.bot.user.edit(avatar=original_avatar, username=original_username)
        await ctx.send("Profilbild und Nutzername wurden geklont.")


    @commands.command()
    async def suser(self, ctx, nutzer_id: int, name: str):
    """ 
    Anwendung: !suser [nutzerID] [Name]
    Speichert das Nutzerprofiel der angegebenen ID um es später zu nutzen.
    [Name] ist der Name der gespeicherten Daten."""
        try:
            user = await self.bot.fetch_user(nutzer_id)
        except discord.NotFound:
            await ctx.send("Nutzer nicht gefunden.")
            return
        filename = f"{name}.txt"
        with open(filename, "w") as f:
            f.write(f"{user.avatar_url}\n{user.name}")
        image_url = user.avatar_url_as(size=256)
        image_filename = f"{name}.png"
        response = requests.get(image_url)
        with open(image_filename, "wb") as f:
            f.write(response.content)
        await ctx.send("Nutzer gespeichert.")


    @commands.command()
    async def users(self, ctx):
    """
    Zeigt die gespeicherten Nutzerprofile an die man mit "!iam" nutzen kann. :o"""
        nutzer_liste = []
        for dateiname, daten in self.gespeicherte_nutzer.items():
            nutzer_liste.append(f"{dateiname}: {daten['name']}")
        if nutzer_liste:
            await ctx.send("Gespeicherte Nutzer:\n" + "\n".join(nutzer_liste))
        else:
            await ctx.send("Keine Nutzer gespeichert.")


    @commands.command()
    async def iam(self, ctx, name: str, zeit: int = None):
    """Anwendung: !iam [name] [Zeit in Minuten (optional)]
       Nutzt das mit "!suser" gespeicherte Nutzerprofil dessen Namen du bei [name] angibst!"""
        if name not in self.gespeicherte_nutzer:
            await ctx.send(f"Ich habe keinen Nutzer mit dem Namen {name} gespeichert.")
            return
        aktueller_name = ctx.author.display_name
        aktuelles_profilbild = await ctx.author.avatar_url.read()
        pfad = self.gespeicherte_nutzer[name]['profilbild']
        with open(pfad, 'rb') as f:
            profilbild = f.read()
        await ctx.author.edit(nick=name)
        await ctx.author.edit(avatar=profilbild)
        if zeit is not None:
            await asyncio.sleep(zeit * 60)
            await ctx.author.edit(nick=aktueller_name)
            await ctx.author.edit(avatar=aktuelles_profilbild)
        await ctx.send("Profilbild und Nutzername wurden geändert.")


def setup(bot):
    bot.add_cog(uclone(bot))
