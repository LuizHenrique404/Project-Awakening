# Aqui estarão as listas de palavras utilizadas para os comandos.
# [    ] <- Espaçamento.

from datetime import datetime

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
    filtoDaFrase = filtoDaFrase.replace("!", "").replace("?", "")
    filtoDaFrase = filtoDaFrase.replace("/", "").replace("<", "")

    return filtoDaFrase

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

# ADICIONAR UM FATOR DE ARMAZENAMENTO DE PERGUNTAS E RESPOSTAS NO DATABASE.

# USER
greetings = ("ola", "oi", "opa", "saudacoes", "ei", "e ai", "fala", "salve", "iae", "coe", "aoba")
greetingsComical = ("fala", "salve", "iae", "coe", "aoba")

# Atualização futura....
charadeCall = ("me responda uma charada", "eu tenho uma charada para voce", "responda a charada", "responda minha charada", 
                "hora da charada", "hora da minha charada", "receba minha charada", "receba a charada", "resolva a charada",
                "resolva a minha charada", "responda uma charada", "hora de responder uma charada", "a charada deverá ser respondida",
                "eu tenho uma charada", "que tal responder a uma charada", "que tal responder a minha charada", "que tal responder uma charada")

# BOT
greetingsCommonResponse = {"formal":["Olá.", "Olá!", ":robot: Saudações!", "Saudações", "Opa!", "Opa."], # 6
                           "coloquial": ["Salve!", "Fala.", "Lata. :dog:", "Aoba!", ":question:", "Iaí rapaz?"], # 6
                           "raivoso": ["Sim?", "O que foi?", "Qual o problema?", "Diga.", "Fale."]} # 5
greetingsResponseUnknown = {"cumprimento":["Olá", "Saudações!", "Opa!"], # 3
                            "apresentação":["Meu nome é Devatron, sou um BOT do discord, mas eu opero além do discord.", 
                            "Eu sou o Devatron, sou uma IA de teste capaz de realizar diversas funções.", "Meu nome é Devatron.", 
                            "Eu sou Devatron.", "Eu sou Devatron, Devatron sou eu.", "Eu sou uma IA de teste, chamado de Devatron!"], # 6
                            "cintinuação": ["Dando continuidade as tarefas...", "Continuando...", "Seguindo...", 
                            "Continuando com o que estavamos fazendo...", "Dando continuidade a nossas tarefas..."]} # 5

lastInteractionResponse = {"Bastante tempo":["A quanto tempo que não nos falamos.", "Nossa, já faz mais de um ano.", "Depois de um ano, ele voltou."], # 3
                           "Um bom tempo":["Faz um certo tempo que você não aparece.", "A quanto tempo. :face_with_monocle:", "A quanto tempo heim. :face_with_raised_eyebrow:"], # 3
                           "Um tempinho":["Long time no see.", "Não te vejo faz um tempinho.", "Já faz um tempo que não nos falamos."]} # 3

lastInteractionResponseComical = {"Bastante tempo":["Olha ele aí, demorou mas voltou.", "O homem finalmente despistou os agiotas.", "O cara tava fugindo da policia, demorou que só.", 
                                                    "O cara só pode ter sido abdusido por ETs pra ter demorado tanto tempo assim.", ":face_with_monocle: Sumiço grande esse seu."], # 5
                                    "Um bom tempo":["Tava demorando.", "Demorou, mas voltou.", "Finalmente, acharam o cara.", "O homem saiu pra férias.", "As férias acabaram foi? :laughing:"], # 5
                                    "Um tempinho":[":wave: Bom dia!", "Espero que o final de semana tenha sido massa. :disguised_face:", "Long time no see. :flag_us: :eagle:", 
                                                   "Hora de voltar a ação, capitão. :saluting_face:", "Good day man! :wave: :flag_us:"]} # 5

charadeCallResponse = {"formal":["Certo, mande sua charada.", "Diga-me sua charada.", "Interessante, diga-me.", "Me surpreenda."], 
                        "coloquial":["Manda a braba. :fire:", "Pode jogar pra cima de mim.", "Quero ver essa potência. :eye::eye:", "Pode ir dizendo."], 
                        "raivoso":["Seja rápido.", "Diga logo.", "Seja pelo menos criativo.", "Hmm."]}
