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


# Commande Discord pour chiffrer/déchiffrer des messages
@bot.command(aliases=["CHIFRER", "chifrer"])
async def Chifrer(ctx):
    # Récupère le serveur (guild) à partir du contexte
    guild = ctx.message.guild

    # Supprime le message de commande d'origine
    await ctx.message.delete()

    # Crée un nouveau canal de texte nommé "canal-de-chiffrage" dans le serveur
    channel = await guild.create_text_channel("canal-de-chiffrage")

    # Définit une fonction pour vérifier si un message provient du même utilisateur et canal
    def SameChannelUser(msg):
        return msg.channel == channel and msg.author == ctx.author

    # Fonction pour générer une paire de clés publique/privée RSA
    # Définir une fonction pour générer des clés RSA
    def generate_keys():
        # Générer deux nombres premiers aléatoires, p et q, dans une plage donnée
        p = random.randint(100000000, 999999999)
        q = random.randint(100000000, 999999999)

        # Tant que p n'est pas premier, incrémentez p jusqu'à ce qu'il le devienne
        while not is_prime(p):
            p += 1

        # Tant que q n'est pas premier, incrémentez q jusqu'à ce qu'il le devienne
        while not is_prime(q):
            q += 1

        # Calculer le produit de p et q, n, qui sera la partie publique de la clé
        n = p * q

        # Calculer la fonction d'Euler de n, phi, utilisée pour la clé privée
        phi = (p - 1) * (q - 1)

        # Générer un nombre aléatoire e dans la plage (2, phi - 1)
        e = random.randint(2, phi - 1)

        # Tant que e et phi ne sont pas premiers entre eux, incrémentez e
        while gcd(e, phi) != 1:
            e += 1

        # Calculer l'inverse modulaire de e modulo phi, d, pour la clé privée
        d = modinv(e, phi)

        # Retourner un tuple contenant la clé publique (e, n) et la clé privée (d, n)
        return (e, n), (d, n)

    # Fonction pour vérifier si un nombre est premier
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    # Fonction pour calculer le PGCD de deux nombres
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    # Fonction pour calculer l'inverse modulaire d'un nombre
    def modinv(a, m):
        g, x, y = gcd(a, m), 0, 1
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return pow(a, -1, m)

    # Fonction pour chiffrer un message avec une clé publique
    def encrypt(message, public_key):
        e, n = public_key
        return [pow(ord(c), e, n) for c in message]

    # Fonction pour déchiffrer un message chiffré avec une clé privée
    def decrypt(ciphertext, private_key):
        d, n = private_key
        return ''.join([chr(pow(c, d, n)) for c in ciphertext])

    # Fonction principale asynchrone
    async def main():
        global private_key

        # Boucle pour interagir avec l'utilisateur
        while True:
            author = ctx.author

            '''Demande à l'utilisateur s'il souhaite créer une paire de clés'''

            await channel.send('Voulez-vous créer une paire de clés? [y/n]')
            choice = await bot.wait_for("message", check=SameChannelUser)
            choice = choice.content
            keyHaBeGe = False

            # Si l'utilisateur choisit de créer une paire de clés
            if choice == 'y':
                # Génère la paire de clés publique/privée
                public_key, private_key = generate_keys()

                # Envoie la clé privée à l'utilisateur en message privé
                dm_chan = await ctx.author.create_dm()
                await dm_chan.send("Clé privée :")
                await dm_chan.send(f"{private_key[0]} {private_key[1]}")
                await dm_chan.send("Clé publique :")
                await dm_chan.send(f"{public_key[0]} {public_key[1]}")

                keyHaBeGe = True

                # Boucle pour gérer le partage de la clé publique
                while True:
                    await dm_chan.send("Voulez-vous partager votre clé publique [y/n]")
                    message = await bot.wait_for("message")
                    choice = message
                    choice = choice.content

                    if choice == 'y':
                        # Partage la clé publique dans le canal actuel
                        await ctx.channel.send("Voici une des clés publiques de " + f"{author.mention}" + ":")
                        await ctx.channel.send(f"{public_key[0]} {public_key[1]}")
                        break
                    elif choice == 'n':
                        await dm_chan.send("ok")
                        break
                    else:
                        await dm_chan.send('Veuillez entrer y ou n')
                break
            # Si l'utilisateur choisit de ne pas créer de clé
            elif choice == 'n':
                break
            else:
                await channel.send("Veuillez entrer y ou n")

        '''Boucle pour chiffrer un message'''

        while True:
            await channel.send('Voulez-vous chiffrer un message? [y/n]')
            choice = await bot.wait_for("message", check=SameChannelUser)
            choice = choice.content

            # Si l'utilisateur choisit de chiffrer un message
            if choice == 'y':
                if keyHaBeGe:
                    # Concaténer les deux éléments de la clé publique en une seule chaîne, séparés par un espace
                    public_key = f"{public_key[0]} {public_key[1]}"
                    # Diviser la chaîne de la clé publique en une liste de chaînes, en utilisant l'espace comme séparateur
                    public_key = public_key.split()
                    # Convertir chaque élément de la liste en un entier en utilisant la fonction map
                    public_key = map(int, public_key)

                    dm_chan = await ctx.author.create_dm()
                    await dm_chan.send('Entrez le message à chiffrer')
                    message = await bot.wait_for("message")
                    message = message.content

                    '''Chiffre le message et envoie le texte chiffré en message privé'''
                    # Chiffrer le message en utilisant la clé publique
                    ciphertext = encrypt(message, public_key)
                    # Envoyer un message dans un canal privé avec le message chiffré
                    await dm_chan.send("Message chiffré: ")
                    # Envoyer le message chiffré
                    await dm_chan.send("" + " ".join(str(x) for x in ciphertext))
                    # Supprimer le canal actuel (channel) (canal_de_cryptage)
                    await channel.delete()
                    break
                elif not keyHaBeGe:
                    # Envoyer un message demandant à l'utilisateur d'entrer la clé publique
                    await channel.send('Entrez la clé publique')
                    # Attendre que l'utilisateur fournisse la clé publique
                    public_key = await bot.wait_for("message", check=SameChannelUser)
                    # Diviser la chaîne de la clé publique en une liste de chaînes en utilisant l'espace comme séparateur
                    public_key = public_key.content.split()
                    # Convertir chaque élément de la liste en un entier en utilisant la fonction map
                    public_key = map(int, public_key)
                    # Créer un canal privé avec l'auteur du message actuel
                    dm_chan = await ctx.author.create_dm()
                    # Envoyer un message dans le canal privé demandant à l'utilisateur d'entrer le message à chiffrer
                    await dm_chan.send('Entrez le message à chiffrer')
                    # Attendre que l'utilisateur fournisse le message à chiffrer
                    message = await bot.wait_for("message")
                    # Extraire le contenu du message
                    message = message.content

                    # Chiffre le message et envoie le texte chiffré en message privé
                    ciphertext = encrypt(message, public_key)
                    await dm_chan.send("Message chiffré: ")
                    await dm_chan.send("" + " ".join(str(x) for x in ciphertext))
                    await channel.delete()
                    break
                else:
                    break
            # Si l'utilisateur choisit de ne pas chiffrer de message
            elif choice == 'n':
                await channel.delete()
                break
            else:
                await channel.send('Veuillez entrer y ou n')

        # Boucle pour déchiffrer un message
        while True:
            dm_chan = await ctx.author.create_dm()
            await dm_chan.send('Voulez-vous déchiffrer un message? [y/n]')
            message = await bot.wait_for("message")
            choice = message
            choice = choice.content

            # Si l'utilisateur choisit de déchiffrer un message
            if choice == 'y':
                if keyHaBeGe:
                    dm_chan = await ctx.author.create_dm()
                    await dm_chan.send("Voulez vous utiliser une autre clé privée [y/n]")
                    message = await bot.wait_for("message")
                    choice = message
                    choice = choice.content

                    # Si l'utilisateur choisit d'utiliser une autre clé privée
                    if choice == 'y':
                        await dm_chan.send('Entrez la clé privée')
                        message = await bot.wait_for("message")
                        private_key = message
                        private_key = private_key.content.split()
                        private_key = map(int, private_key)
                        await dm_chan.send('Entrez le message chiffré')
                        message = await bot.wait_for("message")
                        ciphertext = message
                        ciphertext = ciphertext.content.split()
                        ciphertext = map(int, ciphertext)
                        plaintext = decrypt(ciphertext, private_key)

                        # Envoie le message déchiffré en message privé
                        await dm_chan.send("Le message chiffré est:")
                        await dm_chan.send(f"{plaintext}")
                        break
                    # Si l'utilisateur choisit de ne pas utiliser une autre clé privée
                    elif choice == 'n':
                        private_key = f"{private_key[0]} {private_key[1]}"
                        private_key = private_key.split()
                        private_key = map(int, private_key)
                        await dm_chan.send('Entrez le message chiffré')
                        message = await bot.wait_for("message")
                        ciphertext = message
                        ciphertext = ciphertext.content.split()
                        ciphertext = map(int, ciphertext)
                        plaintext = decrypt(ciphertext, private_key)

                        # Envoie le message déchiffré en message privé
                        await dm_chan.send("Le message chiffré est:")
                        await dm_chan.send(f"{plaintext}")
                        break
                    else:
                        await dm_chan.send('Veuillez entrer y ou n')
                elif not keyHaBeGe:
                    await dm_chan.send('Entrez la clé privée')
                    message = await bot.wait_for("message")
                    private_key = message
                    private_key = private_key.content.split()
                    private_key = map(int, private_key)
                    await dm_chan.send('Entrez le message chiffré')
                    message = await bot.wait_for("message")
                    ciphertext = message
                    ciphertext = ciphertext.content.split()
                    ciphertext = map(int, ciphertext)
                    plaintext = decrypt(ciphertext, private_key)

                    # Envoie le message déchiffré en message privé
                    await dm_chan.send("Le message chiffré est:")
                    await dm_chan.send(f"{plaintext}")
                    break
                else:
                    break
            # Si l'utilisateur choisit de ne pas déchiffrer de message
            elif choice == 'n':
                break
            else:
                await dm_chan.send('Veuillez entrer y ou n')

    # Exécute la fonction principale si ce fichier est exécuté en tant que script principal
    if __name__ == '__main__':
        await main()


@bot.command(aliases=["chifr", "CHIFR"])
async def Chifr(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()

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

    dm_chan = await ctx.author.create_dm()
    await dm_chan.send('Entrez la clé publique')
    public_key = await bot.wait_for("message")
    public_key = public_key.content.split()
    public_key = map(int, public_key)
    await dm_chan.send('Entrez le message à chiffrer')
    message = await bot.wait_for("message")
    message = message.content
    ciphertext = encrypt(message, public_key)
    await dm_chan.send("Message chiffré: ")
    await dm_chan.send("" + " ".join(str(x) for x in ciphertext))


@bot.command(aliases=["DECHIFR", "dechifr"])
async def Dechifr(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()

    def decrypt(ciphertext, private_key):
        d, n = private_key
        return ''.join([chr(pow(c, d, n)) for c in ciphertext])

    while True:
        dm_chan = await ctx.author.create_dm()
        await dm_chan.send('Entrez la clé privé')
        message = await bot.wait_for("message")
        private_ke = message
        private_ke = private_ke.content.split()
        private_ke = map(int, private_ke)
        await dm_chan.send('Entrez le message chiffré')
        message = await bot.wait_for("message")
        ciphertext = message
        ciphertext = ciphertext.content.split()
        ciphertext = map(int, ciphertext)
        plaintext = decrypt(ciphertext, private_ke)
        await dm_chan.send("Le message chiffré est:")
        await dm_chan.send(f"{plaintext}")
        break


@bot.command(aliases=["GENERATE", "Generate"])
async def generate(ctx):
    await ctx.message.delete()

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

    author = ctx.author
    public_key, private_key = generate_keys()
    dm_chan = await ctx.author.create_dm()
    await dm_chan.send("Clé privée :")
    await dm_chan.send(f"{private_key[0]} {private_key[1]}")
    await dm_chan.send("Clé publique :")
    await dm_chan.send(f"{public_key[0]} {public_key[1]}")

    while True:
        await dm_chan.send("Voulez vous partager votre clé publique [y/n]")
        message = await bot.wait_for("message")
        choice = message
        choice = choice.content
        if choice == 'y':
            await ctx.channel.send("Voici une des clés publique de " + f"{author.mention}" + ":")
            await ctx.channel.send(f"{public_key[0]} {public_key[1]}")
            break
        elif choice == 'n':
            await dm_chan.send("ok")
            break
        else:
            await dm_chan.send('Veuillez entrer y ou n')


@bot.event
async def on_message(msg):
    if not msg.author.bot:
        if msg.content == "Ping":
            await msg.channel.send("Pong")

        if msg.content == "ping":
            await msg.channel.send("pong")

    await bot.process_commands(msg)


if __name__ == '__main__':
    bot.run(BOT_TOKEN)
