import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import os


load_dotenv()

urls = os.getenv('urls').split(',')

print(urls)

def get_prices(urls):
    headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(urls, headers=headers)

    if response.status_code == 200:
        soap = BeautifulSoup(response.text, 'html.parser')

        possible_classes = ["price", "product-price", "a-price-whole", "preco", "preco-avista"]

        for class_name in possible_classes:
            price_tag = soap.find(attrs={"itemprop":"price"})
            if price_tag:
                price = price_tag["content"]
                return price

    return "Preço não encontrado"

data = []

for url in urls:
    price = get_prices(url)
    site = url.split("/")[2]
    data.append({"URL": site, "Preço": price})
    print(f"Produto: {url}\nPreço: {price}\n")
    time.sleep(2)

df = pd.DataFrame(data)

df.to_excel("prices.xlsx", index=False)

print("CSV gerado com sucesso!")