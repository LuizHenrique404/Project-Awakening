# Área para a coleta de dados da internet.
# Conteúdo: Significado de palavras, Valores de Cryptomoedas.
# Significado: Ele buscará os significado da palavra enviada pelo usuário em uma página de dicionário.
# Podendo ser corrigido pelo usuário quando o Learning Mode estiver ativado.
# Crypto: Ele enviará, armazenará e fará uma comparação com o valor já armazenado da moéda.

# Site do Dicionário: https://www.dicio.com.br/palavra/
# Site do Crypto: https://coinmarketcap.com/currencies/bitcoin/
from bs4 import BeautifulSoup
import mysql.connector
import requests
import commands

class getInfo():
    cursor = False
    cnx = False

    def __init__(self, cursor, cnx):
        self.cursor = cursor
        self.cnx = cnx

    def dictionary(self, word: str):
        self.cursor.execute(f"SELECT * FROM mind.dictionary WHERE palavra='{word}';")
        db_words = self.cursor.fetchall()

        if db_words:
            return db_words[0][1]
        else:
            response = requests.get(f"https://www.dicio.com.br/{word}/")
            content = BeautifulSoup(response.content, "html.parser")

            dictionaryResponse = content.find("div", attrs={"class":"title-header"})
            dictionaryResponse = dictionaryResponse.find("h1")
            dictionaryResponse = dictionaryResponse.text

            if str(dictionaryResponse) == "Não encontrada":
                return "Não encontrada"
            else:
                wordMeaning = content.find("p", attrs={"class":"significado textonovo"})
                messageResponse = str(commands.filtroDicionario(wordMeaning))

                messageResponse = messageResponse.replace("[", "**[").replace("]", "]**")
                messageResponse = messageResponse.replace("(", "**(").replace(")", ")**")
                messageResponse = messageResponse.replace('"', '**"**')

                self.cursor.execute(f"INSERT INTO mind.dictionary (palavra, significado) VALUES ('{word}', '{messageResponse}');")
                self.cnx.commit()
        return messageResponse
    
    def cryptoCurrency(self, coins: list):
        infoList = list()
        coinNames = list()

        for coin in coins:
            coin = list(coin)
            coin[0] = coin[0].upper()
            coin = "".join(coin)

            if coin in coinNames:
                continue
            coinNames.append(coin)

            response = requests.get(f"https://coinmarketcap.com/currencies/{coin}/")
            content = BeautifulSoup(response.content, "html.parser")

            # Info: Value, Volume, Market Cap, Cash Markets
            # Value: span - sc-d1ede7e3-0 fsQm base-text
            # Market Cap and Volume: dd - sc-d1ede7e3-0 hPHvUM base-text

            try:
                coinValue = content.find("span", attrs={"class":"sc-d1ede7e3-0 fsQm base-text"})
                coinBaseInfo = content.find_all("dd", attrs={"class":"sc-d1ede7e3-0 hPHvUM base-text"})

                coinValue = coinValue.text
                coinValue = coinValue.replace(",", "~").replace(".", ",")
                coinValue = coinValue.replace("~", ".").replace("$", "")

                counter = 0
                for info in coinBaseInfo:
                    info = str(info.text).split("%")[1]
                    info = info.replace(",", "~").replace(".", ",")
                    info = info.replace("~", ".").replace("$", "")

                    if counter == 0:
                        marketCap = info
                    if counter == 1:
                        volume = info
                    if counter == 2:
                        break                
                    counter += 1
                
                infoList.append([coin, coinValue, marketCap, volume])
            except:
                infoList.append(["Não encontrada", coin])
            
        return infoList