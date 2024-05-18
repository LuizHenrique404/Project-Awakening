import commands
import mind

from datetime import datetime
from random import randint
from time import sleep
import mysql.connector
import discord

botToken = "MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GVIJ51.8ejBZn4DTaqWilXrUbEAyuO3WG4DSkxtNhLZXk"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'[{client.user.name}] EU FUI ATIVADO')

@client.event
async def on_message(message):
    usuarioReconhecido = False
    humorDoUsuario = "neutro"
    bom = 0
    comico = 0
    ruim = 0

    print(f"[{message.author.name}] {message.content.replace('<', '')}")
    if message.author == client.user or message.content[0] != "<":
        return
    
    mensagem = commands.filtro(message.content)
    cnx = mysql.connector.connect(user='root', password='pass334', host='localhost', database='mind')
    cursor = cnx.cursor() # FALTA TERMINAR DE CONFIGURAR O MYSQL

    cursor.execute(f"SELECT * FROM mind.users_info WHERE username='{message.author.name.lower()}';")
    usuarioReconhecido = cursor.fetchall()

    if usuarioReconhecido:
        usuarioReconhecido = (usuarioReconhecido[0], 0)
        bom = usuarioReconhecido[0][1]
        comico = usuarioReconhecido[0][2]
        ruim = usuarioReconhecido[0][3]

        resultado = commands.calculoDeTempo(usuarioReconhecido[0][4])
        userHumor = mind.HumorClassification()
        humorDoUsuario = userHumor.getHumor(pontos=(usuarioReconhecido[0][1], usuarioReconhecido[0][2], usuarioReconhecido[0][3]))
    else:
        usuarioReconhecido = ([message.author.name.lower(), 0, 0, 0, datetime.now().date()], 1) # 6 Itens
        await message.channel.send(commands.greetingsResponseUnknown["cumprimento"][randint(0, 2)])
        sleep(0.5)
        await message.channel.send(commands.greetingsResponseUnknown["apresentação"][randint(0, 4)])
        if mensagem.split(" ")[0] not in commands.greetings:
            sleep(0.7)
            await message.channel.send(commands.greetingsResponseUnknown["continuação"][randint(0, 4)])
        cursor.execute(f"INSERT INTO mind.users_info (username, bom, comico, ruim, ultima_interação) VALUES ('{usuarioReconhecido[0][0]}', 0, 0, 0, '{usuarioReconhecido[0][4]}')")
        cnx.commit()
        sleep(0.7)

    # Pedra papel e tesoura estratégico.
    # Adicionar um fator batalha de rap.
    # Adicionar o fator reconhecimento de imagens.
    # Checar o ganho de pontos, e seu balanceamento. (Bom e Cómico)

    if mensagem.split(" ")[0] in commands.greetings:
        bom += 0.1
        if mensagem.split(" ")[0] in commands.greetingsComical:
                bom += 0.05
                comico += 0.2
        sleep(0.5)
        if usuarioReconhecido[1] == 0:
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(commands.greetingsCommonResponse["formal"][randint(0, 5)])
                try:
                    await message.channel.send(commands.lastInteractionResponse[resultado][randint(0, 2)])
                except:
                    pass
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.greetingsCommonResponse["coloquial"][randint(0, 5)])
                try:
                    await message.channel.send(commands.lastInteractionResponseComical[resultado][randint(0, 5)])
                except:
                    pass
            else:
                await message.channel.send(commands.greetingsCommonResponse["raivoso"][randint(0, 4)]) 
    
    if mensagem in commands.computerVisionCall:
        sleep(0.5)
        await message.channel.send("Em desenvolvimento...")

    '''
        for attachement in message.attachments:
            if attachment.content_type.startswith("image"):
               # download the image content
               content = await attachment.read()
    '''
    usuarioReconhecido[1] = commands.equilibroDePontos(bom, comico, ruim)
    cursor.execute(f"UPDATE mind.users_info SET bom={usuarioReconhecido[1][0]}, comico={usuarioReconhecido[1][1]}, ruim={usuarioReconhecido[1][2]}, ultima_interação='{datetime.now().date()}' WHERE username='{usuarioReconhecido[0][0]}'")
    cnx.commit()
    cnx.close()

client.run(token='MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GQvC9b.CrzjjkMBwew8TAOvXZ1wdz6hx3nmIxNK9OXZT0')
