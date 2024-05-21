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
learning_mode = False
contentType = False
question = False
response = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'[{client.user.name}] EU FUI ATIVADO')

@client.event
async def on_message(message):
    usuarioReconhecido = False
    humorDoUsuario = "neutro"
    respondido = False
    bom = 0
    comico = 0
    ruim = 0

    print(f"[{message.author.name}] {message.content.replace('<', '')}")
    if message.author == client.user or message.content[0] != "<":
        if question[1] == message.author.name and response:
            if message.content in ("formal", "comico", "raivoso"):
                contentType = message.content
                commands.armazenamentoDeComandos(contentType, question[0], response)
                contentType = False
                question = False
                response = False
                await message.channel.send("COMANDO ARMAZENADO.")
                print("[SYSTEM] Conteúdo armazenado no DATABASE. (learning_mode)")
            else:
                await message.channel.send("O tom do conteúdo informado deve ser um dos três citados anteriormente. (formal, comico, raivoso)")
        elif question[1] == message.author.name:
            response = message.content

            await message.channel.send("RESPOSTA REGISTRADA.")
            await message.channel.send("Agora informe o tom do conteúdo. (formal, comico, raivoso)")
            await message.channel.send("Todas as letras de sua resposta devem estar minúsculas.")
        else:
            return
    
    mensagem = commands.filtro(message.content)
    cnx = mysql.connector.connect(user='root', password='pass334', host='localhost', database='mind')
    cursor = cnx.cursor()

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
        respondido = True
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
        respondido = True
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
    
    if message.content == "<Learning Mode: True" and message.author.name in commands.admin:
        learning_mode = True
        print("[SYSTEM] LEARNING MODE: True")
        await message.channel.send("**[MODO DE APRENDIZADO ATIVADO]**")
        await message.channel.send("**Question:** Mande um comando para o bot.")
        await message.channel.send("**Response:** Mande a resposta para ser armazenada.")
        await message.channel.send("**ContentType:** Mande o tom do conteúdo.")
        await message.channel.send("Os três tipos serão melhor explicados durante a operação.")
    if message.content == "<Learning Mode: False" and message.author.name in commands.admin:
        learning_mode = False

    if mensagem in commands.computerVisionCall:
        respondido = True
        content = False
        for attachement in message.attachments:
            if attachement.content_type.startswith("image"):
               content = await attachement.read()
               break
        
        if content == False:
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(commands.computerVisionError["formal"][randint(0, 2)])
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.computerVisionError["coloquial"][randint(0, 2)])
            else:
                await message.channel.send(commands.computerVisionError["raivoso"][randint(0, 2)])
        else:
            pass

    if learning_mode and not respondido:
        question = (mensagem, message.author.name)
        await message.channel.send("RESPOSTA NÃO IDENTIFICADA PELO SISTEMA.")
        await message.channel.send("Por favor, envie a resposa mais adequada a este comando.")
        await message.channel.send(r"E utilize **%br%** no caso de duas mensagens ou mais como resposta.")
        await message.channel.send("Exemplo:\n**Mensagem 1:** Provavelmente não... \n**Mensagem 2:** Mas talvez tenha.\nSeria o equivalente a: ",r"Provavelmente não...%br%Mas talvez tenha.")



    bom, comico, ruim = commands.equilibroDePontos(bom, comico, ruim)
    cursor.execute(f"UPDATE mind.users_info SET bom={bom}, comico={comico}, ruim={ruim}, ultima_interação='{datetime.now().date()}' WHERE username='{usuarioReconhecido[0][0]}'")
    cnx.commit()
    cnx.close()

client.run(token='MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GQvC9b.CrzjjkMBwew8TAOvXZ1wdz6hx3nmIxNK9OXZT0')