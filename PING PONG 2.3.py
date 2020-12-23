import discord
from discord.ext import commands
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!", description="bot de Zach")


@bot.event
async def on_ready():
    print("Bonjour je suis pret")


# @bot.event
# async def on_message(msg):
#     if not msg.author.bot:
#         await msg.channel.send("Bonjour!!!")


@bot.event
async def on_message(msg):
    if not msg.author.bot:
        if msg.content == "Au-revoir":
            await msg.channel.send("à bientôt")

    # @bot.event
    # async def on_message(msg):
    #     if not msg.author.bot:
    #         if msg.content == "wuw":
    #             await msg.channel.send("Hooooo_cute")



    await bot.process_commands(msg)


@bot.command()
async def invitation(ctx):
    # await ctx.send("https://discord.gg/cwaCNjf")
    dm_chann = await ctx.author.create_dm()
    await dm_chann.send("https://discord.gg/cwaCNjf")
    await ctx.message.delete()

    @bot.command()
    async def invitation1(ctx):
        # await ctx.send("https://discord.gg/NrHmGXT")
        dm_chann = await ctx.author.create_dm()
        await dm_chann.send("https://discord.gg/NrHmGXT")
        await ctx.message.delete()

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
