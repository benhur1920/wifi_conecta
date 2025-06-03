import pandas as pd


url = 'http://dados.recife.pe.gov.br/dataset/b6f94d98-bc26-46cb-b82b-5fea71c4286a/resource/1329a80b-c4a6-4ecd-b8e5-09ef75ffa576/download/conectarecife.csv'

df = pd.read_csv(url,sep=";", encoding="utf-8")
