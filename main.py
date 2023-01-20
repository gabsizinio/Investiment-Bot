import os
from dotenv import load_dotenv
import tweepy

#import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib as plt

import cloudscraper
import dataframe_image as dfi

import numpy as np

from datetime import date


def get_text(tag_list): 
  data = []
  for tag in tag_list:
    tag = tag.text
    data.append(tag)

  return data

scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
url = 'https://www.suno.com.br/acoes/'
req = scraper.get(url)

# html = req.get("https://www.suno.com.br/acoes/").content
html_parsed = BeautifulSoup(req.content,'html.parser')

cotacoes_maiores_altas = html_parsed.find("div", attrs = {"data-test-id":"quotations-maiores-altas"})
cotacoes_maiores_baixas = html_parsed.find("div",attrs = {"data-test-id":"quotations-maiores-baixas"})

precos_alta_span= cotacoes_maiores_altas.find_all("span", attrs = {"class":"value-market"})
variacao_alta_span = cotacoes_maiores_altas.find_all("span", attrs = {"class":"average up"})
codigos_alta_strong = cotacoes_maiores_altas.find_all("strong")


precos_baixa_strong = cotacoes_maiores_baixas.find_all("strong", attrs = {"class":"value-market"})
variacao_baixa_span = cotacoes_maiores_baixas.find_all("span", attrs = {"class":"average down"})
codigos_baixa_link = cotacoes_maiores_baixas.find_all("a")

"""
 Padronização dos codigos das ações
"""

codigos_alta = get_text(codigos_alta_strong)

codigos_baixa = []
for link in codigos_baixa_link:
  link = link.get("href").replace("/acoes","").replace("/","").upper()
  
  codigos_baixa.append(link)


"""
 Padronização das variacoes dos precos
"""

variacao_alta = get_text(variacao_alta_span)
variacao_baixa = get_text(variacao_baixa_span)

"""
 Padronização dos preços
"""
precos_alta = get_text(precos_alta_span)
precos_baixa = get_text(precos_baixa_strong)

alta_df = pd.DataFrame([variacao_alta,precos_alta], columns = codigos_alta, index = ["Variação", "Preço"])
#dfi.export(alta_df, 'df_styled.png')
baixa_df = pd.DataFrame([variacao_baixa,precos_baixa], columns = codigos_baixa, index = ["Variação", "Preço"])

def create_tweet(tweet,dataframe,var):
  if(var == "baixa"):
    tweet_part = "As Maiores Baixas Do Dia Foram: \n"
  else:
    tweet_part = "As Maiores Altas Do Dia Foram: \n"
  
  for code in dataframe.columns:
    linha_tweet = ""
    variacao,preco = dataframe[code].values[0],dataframe[code].values[1]

    if(var == "baixa"):
      linha_tweet = f'  {code} 💰{preco}  📉 {variacao} \n'
    else:
      linha_tweet = f'  {code} 💰{preco}  📈 {variacao} \n'
  
    tweet_part += linha_tweet
    
  tweet_part += "\n"
  return tweet_part

x = date.today()
post = f"{x.day+1}/{x.month}/{x.year}:\n\n"

tweet_altas = create_tweet(post,alta_df,var = "alta")
post += tweet_altas

tweet_baixas = create_tweet(post,baixa_df,var = "baixa")


#Armazenando as chaves
load_dotenv()

API_KEY = "pXCwX1nrUCDxXsrdgoZk5VdEX"
API_SECRET_KEY = "i4QraUyMWoDfccKlCAtNz4DCSHT8rJGmmkXqY7jsobEBvCSFNn"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOhogQEAAAAAe2tlGB8z22V7kG0UpIMBwHcJBBU%3DC0la8ErkBh3ke2OWIBcnq7NbLgFuWIkkZaE3zbqW8bVJOENRcT"
ACCESS_TOKEN = "1298692051983388676-ruaPIaujU6cWnWLgt6q63ntBwcE67d"
ACCESS_SECRET_TOKEN = "VQXvzjmlBrgWziPM9GvyznT32uLzQbgFzPnEeLFaO3Ev9"



auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_SECRET_TOKEN
)

api = tweepy.API(auth)

post2 = ""
post2 += tweet_baixas

original = api.update_status(status=post)

#time.sleep(30)

reply = api.update_status(status=post2, in_reply_to_status_id = original.id , auto_populate_reply_metadata=True)























'''
api = tweepy.Client(
    consumer_key=API_KEY, 
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET_TOKEN
)


tweet = api.create_tweet(text="SECRET")
'''