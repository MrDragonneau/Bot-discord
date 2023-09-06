import os
import requests
import discord
import random
from discord.ext import commands

BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", description="Bot de Azashire", intents=intents)


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


@bot.command(aliases=["Invitation", "INVITATION", "INVITATIONS", "Invitations", "invitations"])
async def invitation(ctx):
    dm_chan = await ctx.author.create_dm()
    await dm_chan.send("https://discord.gg/6CVXCDvykM")
    await ctx.message.delete()


@bot.command(aliases=["Vdm", "VDM"])
async def vdm(ctx):
    req = requests.get("https://blague.xyz/api/vdm/random")
    req_json = req.json()
    await ctx.channel.send(req_json["vdm"]["content"])


@bot.command(aliases=["Blagues", "blagues", "Blague", "BLAGUES", "BLAGUE"])
async def blague(ctx):
    def SameChannel(msg):
        return msg.channel == ctx.channel

    req = requests.get("https://blague.xyz/api/joke/random")
    req_json = req.json()
    await ctx.channel.send(req_json["joke"]["question"])
    await bot.wait_for("message", check=SameChannel)
    await ctx.channel.send(req_json["joke"]["answer"])


@bot.command(aliases=["Juste_Prix", "JUSTE_PRIX", "juste_prix", "jp"])
async def JP(ctx):
    def SameChannelUser(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author

    p = random.randint(0, 2500)
    running = True
    print(p)
    await ctx.channel.send("Entrer un nombre entier entre 0 et 2500 ")
    tent = 0
    while running:
        tent = tent + 1
        repNb = await bot.wait_for("message", check=SameChannelUser)
        repNb = int(repNb.content)
        if repNb == p:
            await ctx.channel.send(f"Gagné !\nVous avez eu besoin de {tent} tentatives.")
            if tent < 5:
                await ctx.channel.send("Bravo vous êtes très for !!")
            else:
                await ctx.channel.send("Bouuuuhh \"message méprisant\" !!!")
            running = False
        elif repNb > p:
            await ctx.channel.send("C'est moins !")
        elif repNb < p:
            await ctx.channel.send("C'est plus !")



@bot.command(aliases=["CRYPT", "crypt", "krypt", "Krypt", "KRYPT"])
async def Crypt(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()
    channel = await guild.create_text_channel("canal-de-cryptage")


    def SameChannelUser(msg):
        return msg.channel == channel and msg.author == ctx.author

    def generate_keys():
        p = random.randint(100000000, 999999999)
        q = random.randint(100000000, 999999999)
        while not is_prime(p):
            p += 1
        while not is_prime(q):
            q += 1
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randint(2, phi - 1)
        while gcd(e, phi) != 1:
            e += 1
        d = modinv(e, phi)
        return (e, n), (d, n)

    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def modinv(a, m):
        g, x, y = gcd(a, m), 0, 1
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return pow(a, -1, m)

    def encrypt(message, public_key):
        e, n = public_key
        return [pow(ord(c), e, n) for c in message]

    def decrypt(ciphertext, private_key):
        d, n = private_key
        return ''.join([chr(pow(c, d, n)) for c in ciphertext])
    async def mention(ctx, user: discord.User):
        await ctx.send(f"{user.mention}")
    async def main():
        global private_key
        while True:
            author = ctx.author
            await channel.send('Voulez-vous créer une paire de clés? [y/n]')
            choice = await bot.wait_for("message", check=SameChannelUser)
            choice = choice.content
            if choice == 'y':
                keyHaBeGe = 0
                public_key, private_key = generate_keys()
                dm_chan = await ctx.author.create_dm()
                await ctx.channel.send("Voici une des clés publique de " + f"{author.mention}" + ":")
                await ctx.channel.send(f"{public_key[0]} {public_key[1]}")
                await channel.send("Clé publique :")
                await channel.send(f"{public_key[0]} {public_key[1]}")
                await dm_chan.send("Clé privée :")
                await dm_chan.send(f"{private_key[0]} {private_key[1]}")
                await dm_chan.send("Clé publique :")
                await dm_chan.send(f"{public_key[0]} {public_key[1]}")
                keyHaBeGe = 1
                break
            elif choice == 'n':
                break
            else:
                await channel.send("Veuillez entrer y ou n")

        while True:
            await channel.send('Voulez-vous crypter un message? [y/n]')
            choice = await bot.wait_for("message", check=SameChannelUser)
            choice = choice.content
            if choice == 'y':
                if keyHaBeGe == 1:
                    public_key = f"{public_key[0]} {public_key[1]}"
                    public_key = public_key.split()
                    public_key = map(int, public_key)
                    dm_chan = await ctx.author.create_dm()
                    await dm_chan.send('Entrez le message à crypter')
                    message = await bot.wait_for("message")
                    message = message.content
                    ciphertext = encrypt(message, public_key)
                    await dm_chan.send("Message crypté: ")
                    await dm_chan.send("" + " ".join(str(x) for x in ciphertext))
                    await channel.delete()
                    break
                elif keyHaBeGe == 0:
                    await channel.send('Entrez la clé publique')
                    public_key = await bot.wait_for("message", check=SameChannelUser)
                    public_key = public_key.content.split()
                    public_key = map(int, public_key)
                    dm_chan = await ctx.author.create_dm()
                    await dm_chan.send('Entrez le message à crypter')
                    message = await bot.wait_for("message")
                    message = message.content
                    ciphertext = encrypt(message, public_key)
                    await dm_chan.send("Message crypté: ")
                    await dm_chan.send("" + " ".join(str(x) for x in ciphertext))
                    await channel.delete()
                    break
                else:
                    break
            elif choice == 'n':
                await channel.delete()
                break
            else:
                await channel.send('Veuillez entrer y ou n')

        while True:
            dm_chan = await ctx.author.create_dm()
            await dm_chan.send('Voulez-vous décrypter un message? [y/n]')
            message = await bot.wait_for("message")
            choice = message
            choice = choice.content
            if choice == 'y':
                if keyHaBeGe == 1:
                    dm_chan = await ctx.author.create_dm()
                    await dm_chan.send("Voulez vous utiliser une autre clé privé [y/n]")
                    message = await bot.wait_for("message")
                    choice = message
                    choice = choice.content
                    if choice == 'y':
                        await dm_chan.send('Entrez la clé privé')
                        message = await bot.wait_for("message")
                        private_key = message
                        private_key = private_key.content.split()
                        private_key = map(int, private_key)
                        await dm_chan.send('Entrez le message crypté')
                        message = await bot.wait_for("message")
                        ciphertext = message
                        ciphertext = ciphertext.content.split()
                        ciphertext = map(int, ciphertext)
                        plaintext = decrypt(ciphertext, private_key)
                        await dm_chan.send("Le message crypté est:")
                        await dm_chan.send(f"{plaintext}")
                        break
                    elif choice == 'n':
                        private_key = f"{private_key[0]} {private_key[1]}"
                        private_key = private_key.split()
                        private_key = map(int, private_key)
                        await dm_chan.send('Entrez le message crypté')
                        message = await bot.wait_for("message")
                        ciphertext = message
                        ciphertext = ciphertext.content.split()
                        ciphertext = map(int, ciphertext)
                        plaintext = decrypt(ciphertext, private_key)
                        await dm_chan.send("Le message crypté est:")
                        await dm_chan.send(f"{plaintext}")
                        break
                    else:
                        await dm_chan.send('Veuillez entrer y ou n')
                elif keyHaBeGe == 0:
                    await dm_chan.send('Entrez la clé privé')
                    message = await bot.wait_for("message")
                    private_key = message
                    private_key = private_key.content.split()
                    private_key = map(int, private_key)
                    await dm_chan.send('Entrez le message crypté')
                    message = await bot.wait_for("message")
                    ciphertext = message
                    ciphertext = ciphertext.content.split()
                    ciphertext = map(int, ciphertext)
                    plaintext = decrypt(ciphertext, private_key)
                    await dm_chan.send("Le message crypté est:")
                    await dm_chan.send(f"{plaintext}")
                    break
                else:
                    break
            elif choice == 'n':
                break
            else:
                await dm_chan.send('Veuillez entrer y ou n')

    if __name__ == '__main__':
        await main()


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
