from datetime import datetime

print(datetime.now().date())

# Atualização futura....
charadeCall = ("me responda uma charada", "eu tenho uma charada para voce", "responda a charada", "responda minha charada", 
                "hora da charada", "hora da minha charada", "receba minha charada", "receba a charada", "resolva a charada",
                "resolva a minha charada", "responda uma charada", "hora de responder uma charada", "a charada deverá ser respondida",
                "eu tenho uma charada", "que tal responder a uma charada", "que tal responder a minha charada", "que tal responder uma charada")
charadeCallResponse = {"formal":["Certo, mande sua charada.", "Diga-me sua charada.", "Interessante, diga-me.", "Me surpreenda."], 
                        "coloquial":["Manda a braba. :fire:", "Pode jogar pra cima de mim.", "Quero ver essa potência. :eye::eye:", "Pode ir dizendo."], 
                        "raivoso":["Seja rápido.", "Diga logo.", "Seja pelo menos criativo.", "Hmm."]}