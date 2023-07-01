from discord.ext import commands
import os
import requests
import discord

BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", description="bot de Zach", intents=intents)


@bot.event
async def on_ready():
    print("Bonjour je suis pret")


@bot.event
async def on_message(msg):
    if not msg.author.bot:
        if msg.content == "Bonjour":
            await msg.channel.send("Hey")

        if msg.content == "Au-revoir":
            await msg.channel.send("à bientôt")

    await bot.process_commands(msg)


@bot.command()
async def invitation(ctx):
    dm_chan = await ctx.author.create_dm()
    await dm_chan.send("https://discord.gg/6CVXCDvykM")
    await ctx.message.delete()


@bot.command(aliases=["Vdm", "VDM"])
async def vdm(ctx):
    req = requests.get("https://blague.xyz/api/vdm/random")
    req_json = req.json()
    await ctx.channel.send(req_json["vdm"]["content"])


@bot.command(aliases=["Blagues", "blagues", "Blague"])
async def blague(ctx):
    def SameChannel(msg):
        return msg.channel == ctx.channel

    req = requests.get("https://blague.xyz/api/joke/random")
    req_json = req.json()
    await ctx.channel.send(req_json["joke"]["question"])
    await bot.wait_for("message", check=SameChannel)
    await ctx.channel.send(req_json["joke"]["answer"])

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
