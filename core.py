import commands
import mind

from datetime import datetime
from random import randint
from time import sleep
import mysql.connector
import requests
import discord

botToken = "MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GVIJ51.8ejBZn4DTaqWilXrUbEAyuO3WG4DSkxtNhLZXk"

intents = discord.Intents.default()
intents.message_content = True

learning_mode = False
contentType = False
question = False
response = False

thankUsers = list()
user = list()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'[{client.user.name}] EU FUI ATIVADO')

@client.event
async def on_message(message):
    global learning_mode, contentType, question, response, user
    usuarioReconhecido = False
    humorDoUsuario = "neutro"
    respondido = False
    bom = 0
    comico = 0
    ruim = 0

    print(f"[{message.author.name}] {message.content}")
    if message.author == client.user or message.content[0] != "<":
        if message.author.name in user and response:
            if message.content in ("formal", "comico", "ruim", "neutro"):
                contentType = message.content
                commands.armazenamentoDeComandos(contentType, question, response)
                contentType = False
                question = False
                response = False
                await message.channel.send("COMANDO ARMAZENADO.")
                print("[SYSTEM] Conteúdo armazenado no DATABASE. (learning_mode)")
            else:
                await message.channel.send("O tom do conteúdo informado deve ser um dos três já citados. (formal, comico, ruim, neutro)")
            return
        elif message.author.name in user and question:
            response = message.content

            await message.channel.send("RESPOSTA REGISTRADA.")
            await message.channel.send("Agora informe o tom do conteúdo. (formal, comico, ruim, neutro)")
            await message.channel.send("Todas as letras de sua resposta devem estar minúsculas.")
            return
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

    # Adicionar um fator batalha de rap.
    # Adicionar fator histórias aleatórias.
    
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

    if mensagem in commands.imageClassificationCall:
        respondido = True
        content = False

        try:
            image = requests.get(message.attachments[0].url)
            open(f'C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\classificationImage.png', 'wb').write(image.content)

            content = mind.imageClassification()
            print("[SYSTEM] Prediction:", content)

            bom += 0.05
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(f"{commands.imageClassificationResponse["formal"][randint(0, 8)]} {content}")
            elif humorDoUsuario == "comico":
                await message.channel.send(f"{commands.imageClassificationResponse["coloquial"][randint(0, 8)]} {content}")
            else:
                if randint(1, 3) == 1:
                    await message.channel.send(f"{commands.imageClassificationResponse["raivoso"][randint(0, 4)]} {content}")
                else:
                    bom -= 0.05
                    await message.channel.send(commands.badimageClassificationResponse[randint(0, 8)])
        except:
            ruim += 0.1
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(commands.imageOperationsError["formal"][randint(0, 2)])
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.imageOperationsError["coloquial"][randint(0, 2)])
            else:
                ruim += 0.2
                await message.channel.send(commands.imageOperationsError["raivoso"][randint(0, 2)])
    
    # Está sessão deve semrpe estar aqui embaixo nesta ordem.
    cursor.execute(f"SELECT * FROM mind.debug_mode WHERE question='{mensagem}';")
    learnedInfo = cursor.fetchall()

    if learnedInfo:
        # 0 - Question 1 - Response 2 - ContentType
        respondido = True
        learnedInfo = learnedInfo[0]
        
        if learnedInfo[2] == "formal":
            bom += 0.1
        elif learnedInfo[2] == "comico":
            bom += 0.15
            comico += 0.1
        elif learnedInfo[2] == "ruim":
            ruim += 0.15

        if r"%br%" in learnedInfo[1]:
            learnedSeparateResponse = learnedInfo[1].split(r"%br%")

            for texto in learnedSeparateResponse:
                sleep(0.5)
                await message.channel.send(texto)
        else:
            await message.channel.send(learnedInfo[1])

    if message.content == "<Learning Mode: True" and message.author.name in commands.admin:
        if message.author.name in user:
            await message.channel.send("**[MODO DE APRENDIZADO JÁ ATIVADO]**")
        else:
            user.append(message.author.name)
            learning_mode = True
            respondido = True
            print("[SYSTEM] LEARNING MODE: True", user)
            await message.channel.send("**[MODO DE APRENDIZADO ATIVADO]**")
            await message.channel.send("**Question:** Mande um comando para o bot.")
            await message.channel.send("**Response:** Mande a resposta para ser armazenada.")
            await message.channel.send("**ContentType:** Mande o tom do conteúdo.")
            await message.channel.send("Os três tipos serão melhor explicados durante a operação.")
    if message.content == "<Learning Mode: False" and message.author.name in commands.admin:
        await message.channel.send("**[MODO DE APRENDIZADO DESATIVADO]**")
        learning_mode = False
        contentType = False
        question = False
        response = False

        user.remove(message.author.name)

    if  (mensagem in commands.thanks or mensagem.split(" ")[1] in commands.thanks or mensagem.split(" ")[0] in commands.thanks) and message.author.name in thankUsers:
        await message.channel.send("De nada.")
        thankUsers.remove(message.author.name)
    elif mensagem in commands.thanks or mensagem.split(" ")[1] in commands.thanks or mensagem.split(" ")[0] in commands.thanks:
        await message.channel.send(commands.weirdThanksResponse[randint(0, 5)])
    elif respondido == True and message.author.name not in thankUsers:
        thankUsers.append(message.author.name)

    if learning_mode == True and not respondido and message.author.name in user:
        question = mensagem
        await message.channel.send("RESPOSTA NÃO ENCONTRADA NO SISTEMA.")
        await message.channel.send("Por favor, envie a resposa mais adequada a este comando.")
        await message.channel.send(r"E utilize **%br%** no caso de duas mensagens ou mais como resposta.")
        await message.channel.send("Exemplo:\n**Mensagem 1:** Provavelmente não... \n**Mensagem 2:** Mas talvez tenha.")
        await message.channel.send(r"Seria o equivalente a: "r"Provavelmente não...%br%Mas talvez tenha.")

    bom, comico, ruim = commands.equilibroDePontos(bom, comico, ruim)
    cursor.execute(f"UPDATE mind.users_info SET bom={bom}, comico={comico}, ruim={ruim}, ultima_interação='{datetime.now().date()}' WHERE username='{usuarioReconhecido[0][0]}'")
    cnx.commit()
    cnx.close()

client.run(token='MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GQvC9b.CrzjjkMBwew8TAOvXZ1wdz6hx3nmIxNK9OXZT0')
