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

def equilibroDePontos(bom: int, comico: int, ruim: int):
    if bom > 10 or comico > 10 or ruim > 10:
        bom = bom / 10
        ruim = ruim / 10
        comico = comico / 10
    
    if bom < 0.1: bom = 0
    if ruim < 0.1: ruim = 0
    if comico < 0.1: comico = 0

    return (bom, comico, ruim)

# ADICIONAR UM FATOR DE ARMAZENAMENTO DE PERGUNTAS E RESPOSTAS NO DATABASE.

# USER
greetings = ("ola", "oi", "opa", "saudacoes", "ei", "e ai", "fala", "salve", "iae", "coe", "aoba")
greetingsComical = ("fala", "salve", "iae", "coe", "aoba")

computerVisionCall = ("me diga o voce ve", "me diga o que tem na imagem", "o que tem na imagem", "o que voce ve na imagem", 
                      "o que voce enxerga nessa imagem", "o que voce enxerga na imagem", "me diga o que voce enxerga", 
                      "o que voce enxerga aqui", "o que voce ve aqui", "o que voce ve nessa imagem", "o que tem aqui",
                      "o que tem nessa imagem", "me fale o que voce ve", "me fale o que tem na imagem", "me fale o que voce enxerga",
                      "me diga o que voce esta vendo", "me diga o que voce esta enxergando")

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

computerVisionError = {"formal":["Opa! Tem algo de errado, não consigo entender do que o arquivo em questão se trata. Para evitar erros como este anexe o arquivo de imagem a seu comando.",
                                 "Ops! Algo está errado, não estou conseguindo intender do que o arquivo se trata. Tente anexar um arquivo de imagem a seu comando.", 
                                 "Algo está errado, não consigo entender do que se trata o arquivo em questão. Tente anexar a imagem a seu comando, talvez esse seja o problema!"], # 3
                        "coloquial":["Calma aê cara! Eu não tô conseguindo entender do que a imagem (Se for uma imagem) se trata. Tenta anexar ela ao seu comando. Talvez isso ajude.",
                                     "Opa, peraê! Não tô conseguindo entender nada, isso aí é uma imagem? Você mandou alguma? Tenta anexar uma foto ao seu comando.",
                                     "Eu não entendi. Eu não tô entendendo, tem uma imagem pra ser analisada? Você anexou ela ao seu comando, ou algo do tipo?"], # 3
                        "raivoso":["Como eu deveria interpretar isso? Mande um anexo de imagem, se quiser que eu te diga algo.", 
                                   "Tá errado, tá tudo errado. Você não se deu ao trabalho de me enviar o arquivo de imagem direito, se é que você fez isso. Mande anexado ao comando.",
                                   "Sim, certo. Sabe o que eu vejo? Absolutamente nada! Mande a imagem anexada a seu comando, e talvez eu te diga o que tem nela."]}