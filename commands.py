# Aqui estarão as listas de palavras utilizadas para os comandos.
# [    ] <- Espaçamento.

from datetime import datetime
import mysql.connector
import requests

def filtro(brutoDaFrase: str):

    filtoDaFrase = brutoDaFrase.lower()
    filtoDaFrase = filtoDaFrase.replace("á", "a").replace("ã", "a").replace("â", "a")
    filtoDaFrase = filtoDaFrase.replace("ó", "o").replace("ô", "o").replace("õ", "o")
    filtoDaFrase = filtoDaFrase.replace("ú", "u").replace("û", "u")
    filtoDaFrase = filtoDaFrase.replace("í", "i").replace("î", "i")
    filtoDaFrase = filtoDaFrase.replace("é", "e").replace("ê", "e")
    filtoDaFrase = filtoDaFrase.replace("ç", "c")
    
    filtoDaFrase = filtoDaFrase.replace(".", "").replace(",", "").replace(";", "")
    filtoDaFrase = filtoDaFrase.replace("^", "").replace("´", "").replace("'", "")
    filtoDaFrase = filtoDaFrase.replace("!", "").replace("?", "").replace("-", " ")
    filtoDaFrase = filtoDaFrase.replace("/", "").replace("<", "")

    return filtoDaFrase

def armazenamentoDeComandos(contentType: str, question: str, response: str):
    cnx = mysql.connector.connect(user='root', password='pass334', host='localhost', database='mind')
    cursor = cnx.cursor()
    question = filtro(question)

    cursor.execute(f"INSERT INTO mind.debug_mode (question, response, content) VALUES ('{question}', '{response}', '{contentType}');")
    cnx.commit()
    cnx.close()

def calculoDeTempo(ultimaInteracao: str):
    tempoAtual = str(datetime.now().date()).split("-")
    ultimaInteracao = ultimaInteracao.split("-")
    # 0 - Ano / 1 - Mês / 2 - Dia

    anoAntigo = int(ultimaInteracao[0])
    mesAntigo = int(ultimaInteracao[1])
    diaAntigo = int(ultimaInteracao[2])
    anoAtual = int(tempoAtual[0])
    mesAtual = int(tempoAtual[1])
    diaAtual = int(tempoAtual[2])

    if anoAtual > anoAntigo and mesAtual >= mesAntigo:
        return "Bastante tempo"
    elif mesAtual > mesAntigo and diaAtual >= diaAntigo:
        return "Um bom tempo"
    elif diaAtual > (diaAntigo + 6):
        return "Um tempinho"
    else:
        return "Recentemente"

def equilibroDePontos(bom: int, comico: int, ruim: int):
    if bom > 10 or comico > 10 or ruim > 10:
        bom = bom / 10
        ruim = ruim / 10
        comico = comico / 10
    
    if bom < 0.1: bom = 0
    if ruim < 0.1: ruim = 0
    if comico < 0.1: comico = 0

    return (bom, comico, ruim)

def filtroDicionario(wordMeaning):
    botmessage = str()
    meaning = False

    for meanings in wordMeaning:
        if meanings.text != " " and meaning != meanings.text:
            counter = 0
            for char in meanings.text:
                if char != " ":
                    break
                
                counter += 1
            botmessage += meanings.text[counter:] + r"/505/%br%"
            
            meaning = meanings.text
    botmessage = botmessage.split("/505/")
    botmessage[0] = "**" + botmessage[0].upper() + "**"
    botmessage = ''.join(botmessage)
    return botmessage[:-4]


# ADICIONAR UM FATOR DE ARMAZENAMENTO DE PERGUNTAS E RESPOSTAS NO DATABASE.

# AUTHORIZATION
admin = ("the_coder333", "linusdmarc", "m.luffy5404", "bondaismagic")

# USER
thanks = ("valeu", "obrigado", "brigado", "agradeco", "brigada", "obrigada", "obrigadao")
greetings = ("ola", "oi", "opa", "saudacoes", "ei", "e ai", "fala", "salve", "iae", "coe", "aoba")
greetingsComical = ("fala", "salve", "iae", "coe", "aoba")

imageClassificationCall = ("o que e isto", "do que a imagem se trata", "o que ta na imagem", "que isso", "que isso na imagem", "que isso na foto",
                           "que o objeto e esse", "qual e este objeto", "qual e esse objeto", "do que o objeto se trata", "o que o objeto e",
                           "qual o objeto da imagem", "qual o objeto da foto", "me diga o objeto que esta na foto", "me diga o objeto que esta na imagem",
                           "me diga o objeto que esta aqui", "me fale o objeto que esta na imagem", "me fale o objeto que tem na imagem",
                            "me fale o objeto que tem na foto", "que objeto e este", "o que esta na imagem", "o que esta na foto",
                            "o que e isso", "do que esta imagem se trata", "do que essa imagem se trata")

wordMeaningCall = ("o que esta palavra significa", "o que essa palavra significa", "qual o significado dessa palavra", "qual o significado desta palavra",
                   "me diga qual o significado desta palavra", "me diga qual o singificado da palavra", "me diga qual o significado dessa palavra",
                   "qual o significado da palavra", "me diz o significado da palavra", "me diz o significado dessa palavra", "me diz o significado desta palavra",
                   "me diz qual o significado dessa palavra", "me diz qual o significado desta palavra", "me diz qual o significado da palavra",
                   "fale qual o fignificado da palavra", "fale qual o fignificado desta palavra", "fale qual o fignificado dessa palavra", "significado de",
                   "qual o significado que essa palavra tem", "qual o significado que esta palavra tem", "que significado essa palavra tem",
                   "que significado esta palavra tem", "qual o significado de", "significado de", "me diga o significado da palavra")

cryptoCurrencyCall = ("qual o valor da moeda", "qual o valor dessa moeda", "qual o valor desta moeda", "valor do", "valor da", "qual o valor destas moedas",
                      "qual o valor dessas moedas", "me diga o valor da moeda", "me diga o valor dessa moeda", "me diga o valor desta moeda",
                      "me diga o valor das moedas", "me diga o valor destas moedas", "me diga o valor dessas moedas", "qual o valor das moedas",
                      "que valor tem as modeas", "que valor tem a moeda", "qual valor tem essas moedas", "valor de")

# BOT
weirdThanksResponse = ("De nada?", "Ok?", "Tá bom?", "De nada, eu acho.", "Certo?", "Beleza?") # 6

greetingsCommonResponse = {"formal":["Olá.", "Olá!", ":robot: Saudações!", "Saudações", "Opa!", "Opa."], # 6
                           "coloquial": ["Salve!", "Fala.", "Lata. :dog:", "Aoba!", ":question:", "Iaí rapaz?"], # 6
                           "raivoso": ["Sim?", "O que foi?", "Qual o problema?", "Diga.", "Fale."]} # 5
greetingsResponseUnknown = {"cumprimento":["Olá", "Saudações!", "Opa!"], # 3
                            "apresentação":["Meu nome é Devatron, sou um BOT do discord, mas eu opero além do discord.", 
                            "Eu sou o Devatron, sou uma IA de teste capaz de realizar diversas funções.", "Meu nome é Devatron.", 
                            "Eu sou Devatron.", "Eu sou Devatron, Devatron sou eu.", "Eu sou uma IA de teste, chamado de Devatron!"], # 6
                            "cintinuação": ["Dando continuidade as tarefas...", "Continuando...", "Seguindo...", 
                            "Continuando com o que estavamos fazendo...", "Dando continuidade a nossas tarefas..."]} # 5

wordMeaningError = {"formal":["Lamento, mas não consegui encontrar um sentido para esta palavra.", 
                              "Esta palavra e seu respectivo sentido significado não estão registrados em meus sistemas.",
                              "Não consegui encontrar um significado para esta palavra.", "Não fui capaz de encontrar um significado para esta palavra"], # 4
                    "coloquial":["Eu não faço a menor ideia do sentido por trás dessa palavra.", "Eu não sei. Eu não entendi. Isso não tá registrado em meus sistemas.",
                                 "Eu simplesmente não sei, isso não tá registrado em meus sistemas", "Eu também gostaria de saber qual o significado dessa palavra. :sob:"], # 4
                    "raivoso":["Sei lá. Isso não esta registrado.", "Como eu deveria saber? Isso não foi registrado.", 
                               "Eu não sei. Não há registros disso.", "Eu sei lá. Esta palavra e seu significado não foram registrados."]} # 4

lastInteractionResponse = {"Bastante tempo":["A quanto tempo que não nos falamos.", "Nossa, já faz mais de um ano.", "Depois de um ano, ele voltou."], # 3
                           "Um bom tempo":["Faz um certo tempo que você não aparece.", "A quanto tempo. :face_with_monocle:", "A quanto tempo heim. :face_with_raised_eyebrow:"], # 3
                           "Um tempinho":["Long time no see.", "Não te vejo faz um tempinho.", "Já faz um tempo que não nos falamos."]} # 3

lastInteractionResponseComical = {"Bastante tempo":["Olha ele aí, demorou mas voltou.", "O homem finalmente despistou os agiotas.", "O cara tava fugindo da policia, demorou que só.", 
                                                    "O cara só pode ter sido abdusido por ETs pra ter demorado tanto tempo assim.", ":face_with_monocle: Sumiço grande esse seu."], # 5
                                    "Um bom tempo":["Tava demorando.", "Demorou, mas voltou.", "Finalmente, acharam o cara.", "O homem saiu pra férias.", "As férias acabaram foi? :laughing:"], # 5
                                    "Um tempinho":[":wave: Bom dia!", "Espero que o final de semana tenha sido massa. :disguised_face:", "Long time no see. :flag_us: :eagle:", 
                                                   "Hora de voltar a ação, capitão. :saluting_face:", "Good day man! :wave: :flag_us:"]} # 5

imageClassificationResponse = {"formal":["Acredito que isso seja uma", "Pelo que eu entendi isso é uma", "De acordo com o que eu entendi, isso é uma", 
                                         "Se eu entendi direito, isso é uma", "Espero não estar errado, mas acredito que isso seja uma",
                                         "Pelo o que eu estou vendo, isso é uma", "Posso estar errado, mas acredito que seja uma",
                                         "Da forma que eu entendi, acredito que seja uma", "Pelo que eu vi, isso é uma"], # 9
                               "coloquial":["Rapaz, isso é uma", "Rapaz, pelo que eu tô intendendo isso é uma", ":rofl:  Isso é muito uma",
                                            "Se pá isso é uma", "Do jeito que eu tô vendo, isso é claramente uma", r"Isso é 100% uma",
                                            ":point_up::nerd::sweat_drops: De acordo com os meus cálculos isto é uma",
                                            ":rolling_eyes: Claramente uma", "Você ainda pergunta? Isso é obviamente uma"], # 9
                               "raivoso":["Sei lá. Talvez uma", "Uma", "Talvez uma", "Provavelmente uma", 
                                          "Pelo que eu vi, uma", "Pelo que estou vendo, uma"]} # 5

badimageClassificationResponse = ["Sei lá...", "Não me interessa.", "Não é problema meu.", 
                                  "Você já sabe o que tem.", "Olhe para a imagem que você enviou e me diga.",
                                  "De você, já sei que não vale a pena olhar.", "Não é como se eu me importasse o bastante para dizer.",
                                  "Hmmm.", "Não se preocupe, não vou te dizer.", "Não tô muito afim de perder meu tempo com isso desta vez."] # 9

# PREDICTION
objectDetectionNames = ['chave-inglesa.', 'tesoura.', 'vassoura.']

imageOperationsError = {"formal":["Opa! Tem algo de errado, não consigo entender do que o arquivo em questão se trata. Para evitar erros como este anexe o arquivo de imagem a seu comando.",
                                 "Ops! Algo está errado, não estou conseguindo entender do que o arquivo se trata. Tente anexar um arquivo de imagem a seu comando.", 
                                 "Algo está errado, não consigo entender do que se trata o arquivo em questão. Tente anexar a imagem a seu comando, talvez esse seja o problema!"], # 3
                        "coloquial":["Calma aê cara! Eu não tô conseguindo entender do que a imagem (Se for uma imagem) se trata. Tenta anexar ela ao seu comando. Talvez isso ajude.",
                                     "Opa, peraê! Não tô conseguindo entender nada, isso aí é uma imagem? Você mandou alguma? Tenta anexar uma foto ao seu comando.",
                                     "Eu não entendi. Eu não tô entendendo, tem uma imagem pra ser analisada? Você anexou ela ao seu comando, ou algo do tipo?"], # 3
                        "raivoso":["Como eu deveria interpretar isso? Mande um anexo de imagem, se quiser que eu te diga algo.", 
                                   "Tá errado, tá tudo errado. Você não se deu ao trabalho de me enviar o arquivo de imagem direito, se é que você fez isso. Mande anexado ao comando.",
                                   "Sim, certo. Sabe o que eu vejo? Absolutamente nada! Mande a imagem anexada a seu comando, e talvez eu te diga o que tem nela."]}

