import discord
from discord.ext import commands

class kleinlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cl(self, ctx, limit: int, channel: discord.TextChannel, user: discord.Member = None):
        """
        Anwendung: !cl [Anzahl] [kanalID] [nutzerID(optional)]
        Sende eine Log.txt mit der [Anzahl] der angegebenen Nachrichten aus dem Kanal, in dem der Befehl ausgeführt wird, an den Kanal mit der angegebenen ID. Du kannst optional einen Nutzer mit der ID [nutzerID] angeben, der gefiltert werden soll.
        """

        await ctx.message.delete()  # deletes the command message

        # get messages to log
        messages = []
        async for message in channel.history(limit=limit):
            if user:
                if message.author == user:
                    messages.append(message)
            else:
                messages.append(message)

        # create loading bar
        loading_bar_length = 20
        total_messages = len(messages)
        current_message = 0
        loading_text = "Copying messages to log.txt: "
        loading_bar = "[" + " " * loading_bar_length + "]"
        loading_message = await ctx.send(loading_text + loading_bar)

        # copy messages to log.txt
        with open("log.txt", "w", encoding="utf-8") as f:
            for message in reversed(messages):
                line = f"{message.created_at} - {message.author.name}#{message.author.discriminator}: {message.content}\n"
                f.write(line)
                current_message += 1

                # update loading bar
                percentage = int(current_message / total_messages * 100)
                filled_blocks = int(percentage / (100 / loading_bar_length))
                loading_bar = "[" + "█" * filled_blocks + " " * (loading_bar_length - filled_blocks) + "]"
                loading_text = f"Copying messages to log.txt: {percentage}% {loading_bar}"
                await loading_message.edit(content=loading_text)

        # send log.txt to specified channel
        await channel.send(file=discord.File("log.txt"))

        # delete log.txt
        import os
        os.remove("log.txt")

        # delete command message
        await asyncio.sleep(3)  # wait 3 seconds to make sure file is sent before deleting command message
        await loading_message.delete()

def setup(bot):
    bot.add_cog(kleinlog(bot))
