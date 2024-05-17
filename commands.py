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

def calculoDeTempo(ultimaInteracao: list):
    tempoAtual = str(datetime.now().date()).split("-")
    # 0 - Ano / 1 - Mês / 2 - Dia

    if tempoAtual[0] > ultimaInteracao[0]:
        return "Bastante tempo"
    elif tempoAtual[1] > ultimaInteracao[1]:
        return "Um bom tempo"
    elif tempoAtual[2] > (ultimaInteracao[2] + 6):
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
greetingsCommonResponse = {"formal":["Olá", "Olá!", ":robot: Saudações!", "Saudações", "Opa!", "Opa"], # 6
                           "coloquial": ["Salve!", "Fala", "Lata :dog:", "Aoba!", ":question:", "Iaí rapaz?"], # 6
                           "raivoso": ["Sim?", "O que foi?", "Qual o problema?", "Diga", "Fale"]} # 5
greetingsResponseUnknown = {"cumprimento":["Olá", "Saudações", "Opa!"], # 3
                            "apresentação":["Meu nome é Devatron, sou um BOT do discord, mas eu opero além do discord", 
                            "Eu sou o Devatron, sou uma IA de teste capaz de realizar diversas funções", "Meu nome é Devatron", 
                            "Eu sou Devatron", "Eu sou Devatron, Devatron sou eu", "Eu sou uma IA de teste, chamado de Devatron!"], # 6
                            "cintinuação": ["Dando continuidade as tarefas...", "Continuando...", "Seguindo...", 
                            "Continuando com o que estavamos fazendo...", "Dando continuidade a nossas tarefas..."]} # 5

charadeCallResponse = {"formal":["Certo, mande sua charada", "Diga-me sua charada", "Interessante, diga-me", "Me surpreenda"], 
                        "coloquial":["Manda a braba :fire:", "Pode jogar pra cima de mim", "Quero ver essa potência :eye::eye:", "Pode ir dizendo"], 
                        "raivoso":["Seja rápido", "Diga logo", "Seja pelo menos criativo", "Hmm"]}
