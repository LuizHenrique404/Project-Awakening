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

class getInfo():
    def dictionary(word: str):
        response = requests.get(f"https://www.dicio.com.br/{word}/")
        content = BeautifulSoup(response.content, "html.parser")

        dictionaryResponse = content.find("div", attrs={"class":"title-header"})

        return 0
    def cryptoCurrency(coin: str):
        return 0
    
    def setWordToDictionary(word: str):
        return 0