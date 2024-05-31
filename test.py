from bs4 import BeautifulSoup
import mysql.connector
import requests

response = requests.get(f"https://www.dicio.com.br/bruh/")
content = BeautifulSoup(response.content, "html.parser")

dictionaryResponse = content.find("div", attrs={"class":"title-header"})
dictionaryResponse = dictionaryResponse.find("h1")
dictionaryResponse = dictionaryResponse.text

if str(dictionaryResponse) == "Não encontrada":
    print("Não encontrada")
else:
    print("Encontrada")

'''    Response = requests.get(U)
    Content = BeautifulSoup(Response.content, "html.parser")
        # v Will store all the html content of the products
    Content = Content.find_all("div", attrs={"class":"ui-search-result__content-wrapper shops__result-content-wrapper"})

    for C in Content:       # v Will store the product title
        Title = C.find("div", attrs={"class":"ui-search-item__group ui-search-item__group--title shops__items-group"}).h2
        Price = C.find("span", attrs={"class":"price-tag-fraction"}) # < Will store the product price

        if "Kingston" in str(Title.text) and Price:
            try:
                Data["Title"].append(str(Title.text).strip()) # < Will add the values
                Data["Price"].append(float(Price.text))
            except:
                Data.update({"Title": [str(Title.text).strip()]}) # < Will create the values
                Data.update({"Price": [float(Price.text)]})'''