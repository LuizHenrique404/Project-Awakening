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
    bom = db_bom = 0
    comico = db_comico = 0
    ruim = db_ruim = 0

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
        resultado = commands.calculoDeTempo(usuarioReconhecido[0][4])
        userHumor = mind.HumorClassification()
        humorDoUsuario = userHumor.getHumor(pontos=(usuarioReconhecido[0][1], usuarioReconhecido[0][2], usuarioReconhecido[0][3]))
    else:
        usuarioReconhecido = (message.author.name.lower(), 0, 0, 0, datetime.now().date(), 1) # 6 Itens
        await message.channel.send(commands.greetingsResponseUnknown["cumprimento"][randint(0, 2)])
        sleep(0.5)
        await message.channel.send(commands.greetingsResponseUnknown["apresentação"][randint(0, 4)])
        if mensagem.split(" ")[0] not in commands.greetings:
            sleep(0.7)
            await message.channel.send(commands.greetingsResponseUnknown["continuação"][randint(0, 4)])
        cursor.execute(f"INSERT INTO mind.users_info (username, bom, comico, ruim, ultima_interação) VALUES ('{message.author.name.lower()}', 0, 0, 0, '{datetime.now().date()}')")
        cnx.commit()
        sleep(0.7)

    # Pedra papel e tesoura estratégico.
    # Adicionar um fator batalha de rap.
    # Adicionar o fator reconhecimento de imagens.
    # Checar o ganho de pontos, e seu balanceamento. (Bom e Cómico)

    if mensagem.split(" ")[0] in commands.greetings:
        bom = 0.1
        if mensagem.split(" ")[0] in commands.greetingsComical:
                bom = 0.15
                comico = 0.2

        sleep(0.5)
        if usuarioReconhecido[1] == 0:
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(commands.greetingsCommonResponse["formal"][randint(0, 5)])
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.greetingsCommonResponse["coloquial"][randint(0, 5)])
            else:
                await message.channel.send(commands.greetingsCommonResponse["raivoso"][randint(0, 4)]) 
    cursor.execute(f"UPDATE mind.users_info SET bom={bom}, comico={comico}, ruim={ruim}, ultima_interação='{datetime.now().date()}' WHERE username='{message.author.name.lower()}'")
    cnx.commit()
    cnx.close()

client.run(token='MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GQvC9b.CrzjjkMBwew8TAOvXZ1wdz6hx3nmIxNK9OXZT0')
