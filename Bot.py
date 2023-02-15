import tweepy
import cloudscraper
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd


class twitterBot(tweepy.OAuth1UserHandler):
 
  def __init__(self,API_KEY,API_SECRET_KEY ,ACCESS_TOKEN,ACCESS_SECRET_TOKEN):
    # self.auth = tweepy.OAuth1UserHandler(API_KEY,API_SECRET_KEY ,ACCESS_TOKEN,ACCESS_SECRET_TOKEN)
    super().__init__(API_KEY,API_SECRET_KEY ,ACCESS_TOKEN,ACCESS_SECRET_TOKEN)
    self.api = tweepy.API(self)
  

  def extract_data(self):
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

    codigos_alta = self.get_text(codigos_alta_strong)

    codigos_baixa = []
    for link in codigos_baixa_link:
      link = link.get("href").replace("/acoes","").replace("/","").upper()
      
      codigos_baixa.append(link)



    """
    Padronização das variacoes dos precos
    """

    variacao_alta = self.get_text(variacao_alta_span)
    variacao_baixa = self.get_text(variacao_baixa_span)

    """
    Padronização dos preços
    """
    precos_alta = self.get_text(precos_alta_span)
    precos_baixa = self.get_text(precos_baixa_strong)


    alta_df = pd.DataFrame([variacao_alta,precos_alta], columns = codigos_alta, index = ["Variação", "Preço"])
    baixa_df = pd.DataFrame([variacao_baixa,precos_baixa], columns = codigos_baixa, index = ["Variação", "Preço"])

    return alta_df,baixa_df

  def get_text(self,tag_list): 
    data = []
    for tag in tag_list:
      tag = tag.text
      data.append(tag)

    return data

  def create_tweet(self,tweet,dataframe,var):
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
    
  def send_tweet(self):

    alta_df,baixa_df = self.extract_data()
    today_date = date.today()
    post = f"{today_date.day}/{today_date.month}/{today_date.year}:\n\n"

    tweet_altas = self.create_tweet(post,alta_df,var = "alta")
    tweet_baixas = self.create_tweet(post,baixa_df,var = "baixa")

    

    try:
      post += tweet_altas
      original = self.api.update_status(status = post)

      post2 = ""
      post2 += tweet_baixas

      reply = self.api.update_status(status=post2, in_reply_to_status_id = original.id , 
      auto_populate_reply_metadata=True)

      print("Tweet Posted!!")
      
    except Exception as e:
      print(e)
