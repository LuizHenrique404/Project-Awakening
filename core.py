import commands
import coleta
import mind

from datetime import datetime
from random import randint
from time import sleep
import mysql.connector
import requests
import discord


# ULTIMAS ATUALIZAÇÕES
# -OTIMIZAR AS OPERAÇÕES
# -CHECAGEM FLEXIBILIDADE DAS INTERAÇÕES
# -CHECAGEM NA IMPORTÂNCIA E REAÇÃO DOS PONTOS
# -AUMENTAR A PRECISÃO DA CLASSIFICAÇÃO DAS IMAGENS

botToken = "MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GVIJ51.8ejBZn4DTaqWilXrUbEAyuO3WG4DSkxtNhLZXk"

intents = discord.Intents.default()
intents.message_content = True

learning_mode = False
contentType = False
question = False
response = False
word = False

thankUsers = list()
user = [[],[]]

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'[{client.user.name}] EU FUI ATIVADO')

@client.event
async def on_message(message):
    global learning_mode, contentType, question, response, user, word
    usuarioReconhecido = False
    humorDoUsuario = "neutro"
    respondido = False
    bom = 0
    comico = 0
    ruim = 0

    print(f"[{message.author.name}] {message.content}")
    if message.author == client.user or message.content[0] != "<" or ruim >= 9.5:
        if message.author.name in user[1]:
            meaning = str(message.content)

            cnx = mysql.connector.connect(user='root', password='pass334', host='localhost', database='mind')
            cursor = cnx.cursor()

            cursor.execute(f"INSERT INTO mind.dictionary (palavra, significado) VALUES ('{word}', '{meaning}');")
            cnx.commit()
            cnx.close()

            await message.channel.send("SIGNIFICADO DE PALAVRA REGISTRADO.")
            user[1].remove(message.author.name)
            word = False
            return

        if message.author.name in user[0] and response:
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
        elif message.author.name in user[0] and question:
            response = message.content

            await message.channel.send("RESPOSTA REGISTRADA.")
            await message.channel.send("Agora informe o tom do conteúdo. (formal, comico, ruim, neutro)")
            await message.channel.send("Todas as letras de sua resposta devem estar minúsculas.")
            return
        else:
            return
    
    mensagem = commands.filtro(message.content)
    print(mensagem.split(" ")[0])
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
        if mensagem.split(" ")[0] in commands.greetingsComical:
            bom += 0.05
            comico += 0.2

        usuarioReconhecido = ([message.author.name.lower(), 0, 0, 0, datetime.now().date()], 1) # 6 Itens
        await message.channel.send(commands.greetingsResponseUnknown["cumprimento"][randint(0, 2)])
        sleep(0.5)
        await message.channel.send(commands.greetingsResponseUnknown["apresentação"][randint(0, 4)])
        if mensagem.split(" ")[0] not in commands.greetings:
            respondido = False
            sleep(0.7)
            await message.channel.send(commands.greetingsResponseUnknown["continuação"][randint(0, 4)])
        bom += 0.1
        cursor.execute(f"INSERT INTO mind.users_info (username, bom, comico, ruim, ultima_interação) VALUES ('{usuarioReconhecido[0][0]}', 0, 0, 0, '{usuarioReconhecido[0][4]}')")
        cnx.commit()
        sleep(0.7)
    
    if mensagem.split(" ")[0] == "help":
        respondido = True
        sleep(0.5)
        await message.channel.send("**[COMANDOS DO SISTEMA]**")
        await message.channel.send("Para poder realizar um comando, você sempre deve utilizar o caractere **<** no começo do comando.")
        sleep(0.5)
        await message.channel.send(file=discord.File("Bot_Media\\cmd-command.gif"))
        await message.channel.send("O mesmo comando pode ser escrito de diferentes maneiras, contanto que esteja escrita de maneira correta, o bot conseguirá ler e interpretar normalmente.")
        sleep(0.5)
        await message.channel.send("**<Saudação** - Cummprimentar o Bot.")
        await message.channel.send(".  Exemplo: <Olá")
        sleep(0.2)
        await message.channel.send("**<Agradecimento** - Agradecer ao Bot por alguma ação.")
        await message.channel.send(".  Exemplo: <Obrigado")
        sleep(0.2)
        await message.channel.send("**<Questionamento de classificação** - Classificação de uma imagem.")
        await message.channel.send(".  Exemplo: <Do que a imagem se trata?")
        sleep(0.2)
        await message.channel.send("**<Questionamento de significado** - Descrição de significado de palavras.")
        await message.channel.send(".  Exemplo: <O que significa: Palavra?")
        sleep(0.2)
        await message.channel.send("**<Questionamento de valor** - Descrição do valor da criptomoeda.")
        await message.channel.send(".  Exemplo: <Qual o valor atual do: Bitcoin?")
        
        await message.channel.send("**[COMANDOS GERAIS]**")
        await message.channel.send("**[**Os comandos gerais, são comandos que não foram predefinidos diretamente no sistema, tendo sido imputados por outros usuários durante modo de aprendizado.")
        await message.channel.send(file=discord.File("Bot_Media\\order-complexity.gif"))
        sleep(0.5)
        await message.channel.send("**[**Então não há uma maneira especifica de listar cada um, e sua finalidade, já que são comandos com respostas simples.")
        await message.channel.send("Um exemplo sendo: <The cake is a lie")
        await message.channel.send("**Resposta finalizada.**")


    
    if mensagem.split(" ")[0] in commands.greetings and respondido == False:
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
                    sleep(0.5)
                    await message.channel.send(commands.lastInteractionResponse[resultado][randint(0, 2)])
                except:
                    pass
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.greetingsCommonResponse["coloquial"][randint(0, 5)])
                try:
                    sleep(0.5)
                    await message.channel.send(commands.lastInteractionResponseComical[resultado][randint(0, 5)])
                except:
                    pass
            else:
                await message.channel.send(commands.greetingsCommonResponse["raivoso"][randint(0, 4)])

    if mensagem.split(":")[0] in commands.wordMeaningCall:
        respondido = True

        getWord = coleta.getInfo(cursor, cnx)
        word = mensagem.split(":")[1].replace(" ", "").lower()
        print(word)

        result = getWord.dictionary(word)
        if result == "Não encontrada":
            if learning_mode == True:
                user[1].append(message.author.name)

                await message.channel.send("SIGNIFICADO NÃO ENCONTRADO.")
                await message.channel.send("Por favor informe qual seria a resposta mais adequada.")
                await message.channel.send(r"Lembre-se de fazer a separação de mensagens utilizando %br%")
                await message.channel.send(r"Exemplo: Talvez%br%Seja")
                await message.channel.send("Talvez")
                await message.channel.send("Seja")
            else:
                if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                    await message.channel.send(commands.wordMeaningError["formal"][randint(0, 3)])
                elif humorDoUsuario == "comico":
                    await message.channel.send(commands.wordMeaningError["coloquial"][randint(0, 3)])
                else:
                    await message.channel.send(commands.wordMeaningError["raivoso"][randint(0, 3)])
        else:
            if r"%br%" in result:
                wordSeparateResponse = result.split(r"%br%")

                for meanings in wordSeparateResponse:
                    try:
                        await message.channel.send(meanings)
                    except:
                        continue
            else:
                await message.channel.send(result)
            await message.channel.send("**Resposta finalizada.**")

    if mensagem.split(":")[0] in commands.cryptoCurrencyCall:
        respondido = True
        coins = mensagem.split(":")[1]
        coins = coins[1:].replace(" ", "-").split("/")

        allInfo = coleta.getInfo(cursor, cnx)
        allInfo = allInfo.cryptoCurrency(coins)

        for info in allInfo:
            if info[0] == "Não encontrada":
                ruim += 0.2
                await message.channel.send(f"Não foram encontradas informações sobre {info[1]}...")
            else:
                cursor.execute(f"SELECT * FROM mind.crypto WHERE coinName='{info[0]}';")
                oldInfo = cursor.fetchall()

                sleep(0.5)
                await message.channel.send(f"**[Informações sobre {info[0]} no mercado]**")
                await message.channel.send(f"**o-** Valor da moeda atualmente: ${info[1]}")
                await message.channel.send(f"**o-** Valor de mercado atualmente: ${info[2]}")
                await message.channel.send(f"**o-** Volume atual: ${info[3]}")

                if oldInfo:
                    oldInfo = oldInfo[0]
                    sleep(0.5)
                    await message.channel.send("-")
                    await message.channel.send(f"**o-** Valor antigo da moeda: ${oldInfo[1]}")
                    await message.channel.send(f"**o-** Valor antigo de mercado: ${oldInfo[2]}")
                    await message.channel.send(f"**o-** Volume antigo: ${oldInfo[3]}")
                    
                    valorAtual = info[1].replace(".", "").replace(",", ".")
                    valorAntigo = oldInfo[1].replace(".", "").replace(",", ".")
                    comparacao = float(valorAtual) - float(valorAntigo)

                    if comparacao > 1 or  comparacao < -1:
                        await message.channel.send("-")
                        await message.channel.send(f"Comparação do valor antigo com o atual: {comparacao}")
                try:
                    cursor.execute(f"INSERT INTO mind.crypto (coinName, Value, Volume, MarketCap) VALUES ('{info[0]}', '{info[1]}', '{info[2]}', '{info[3]}');")
                    cnx.commit()
                except:
                    cursor.execute(f"UPDATE mind.crypto SET Value = '{info[1]}', Volume = '{info[2]}', MarketCap = '{info[3]}' WHERE (coinName = '{info[0]}');")
                    cnx.commit()
        await message.channel.send("**Resposta finalizada.**")

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
                try:
                    sleep(0.5)
                    await message.channel.send(commands.lastInteractionResponse[resultado][randint(0, 2)])
                except:
                    pass
            elif humorDoUsuario == "comico":
                try:
                    sleep(0.5)
                    await message.channel.send(commands.lastInteractionResponse[resultado][randint(0, 2)])
                except:
                    pass
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
    try:
        cursor.execute(f"SELECT * FROM mind.learning_mode WHERE question='{mensagem}';")
        learnedInfo = cursor.fetchall()
    except:
        learnedInfo = False

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
        if message.author.name in user[0] or message.author.name in user[1]:
            await message.channel.send("**[MODO DE APRENDIZADO JÁ ATIVADO]**")
        else:
            user[0].append(message.author.name)
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
        await message.channel.send("Todos os registros envolvendo questionamentos e respostas foram apagados.")
        learning_mode = False
        contentType = False
        question = False
        response = False

        user[0].remove(message.author.name)

    try:
        if  (mensagem.split(" ")[0] in commands.thanks or mensagem.split(" ")[1] in commands.thanks) and message.author.name in thankUsers:
            if humorDoUsuario == "bom" or humorDoUsuario == "neutro":
                await message.channel.send(commands.thankResponse["formal"][randint(0, 3)])
            elif humorDoUsuario == "comico":
                await message.channel.send(commands.thankResponse["coloquial"][randint(0, 3)])
            else:
                ruim += 0.2
                await message.channel.send(commands.thankResponse["raivoso"][randint(0, 3)])
            respondido = True
            thankUsers.remove(message.author.name)

        elif mensagem.split(" ")[0] in commands.thanks or mensagem.split(" ")[1] in commands.thanks:
            ruim += 0.05
            await message.channel.send(commands.weirdThanksResponse[randint(0, 5)])

        elif respondido == True and message.author.name not in thankUsers:
            thankUsers.append(message.author.name)
    except:
        pass

    if learning_mode == True and not respondido and message.author.name in user[0]:
        question = mensagem
        await message.channel.send("RESPOSTA NÃO ENCONTRADA NO SISTEMA.")
        await message.channel.send("Por favor, envie a resposa mais adequada a este comando.")
        await message.channel.send(r"E utilize **%br%** no caso de duas mensagens ou mais como resposta.")
        await message.channel.send("Exemplo:\n**Mensagem 1:** Provavelmente não... \n**Mensagem 2:** Mas talvez tenha.")
        await message.channel.send(r"Seria o equivalente a: "r"Provavelmente não...%br%Mas talvez tenha.")

    bom, comico, ruim = commands.equilibroDePontos(bom, comico, ruim)

    print("[Devatron] FIM DO PROCESSO")
    cursor.execute(f"UPDATE mind.users_info SET bom={bom}, comico={comico}, ruim={ruim}, ultima_interação='{datetime.now().date()}' WHERE username='{usuarioReconhecido[0][0]}'")
    cnx.commit()
    cnx.close()

client.run(token='MTIxNjgxNjU4Mjg0MDU0OTM4Nw.GQvC9b.CrzjjkMBwew8TAOvXZ1wdz6hx3nmIxNK9OXZT0')