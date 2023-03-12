import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, self_bot=True)

async def print_loading_bar():
    bar_width = 50
    for i in range(1, 101):
        await asyncio.sleep(0.05)
        bar = "[" + "█" * int(i / 2) + "#" * (bar_width - int(i / 2)) + "]"
        percentage = f"{i}%"
        loading_text = f"bXsxTXx Bot-Menü injecting.... {percentage} {bar}"
        print(loading_text, end="\r", flush=True)
    print("\nInject abgeschlossen. Lade Konfiguration....")
    await asyncio.sleep(3)

async def change_status():
    await client.wait_until_ready()
    statuses = ["T-DC Botmenü soon! c:", "bXsxTXx BotMenü c:"]
    index = 0
    while not client.is_closed():
        await client.change_presence(activity=discord.Game(name=statuses[index]))
        print(f"Changed status to {statuses[index]}")
        index = (index + 1) % len(statuses)
        await asyncio.sleep(60)

@client.event
async def on_ready():
    await print_loading_bar()
    client.load_extension("uclone")
    client.load_extension("kleinlog")


banner = """

		     ~By Bastixx.Inc & ChatGPT~
		         !!!Alpha Version!!!"""
client.run("NTE0OTA3MjM0NjQ0MzkzOTk2.Gi0SpK.yO3mE8Y7uMMVWMspOUqKkccsQSJ8zhcE-C1cSU", bot=False)
