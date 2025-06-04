from dataset import df
import pandas as pd
import streamlit as st
import re


# Verificar os valores únicos da coluna 'bairro'
bairros_ordenados = df['BAIRRO'].sort_values().unique()

# Função para limpar os dados 
def limpar_dados(df):
    substituicoes = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'Ã': 'A', 'Õ': 'O', 'Â': 'A', 'Ç': 'C', 'Ô': 'O', 'Ë':'E'
    }

    df['BAIRRO'] = df['BAIRRO'].replace(substituicoes, regex=True)

    df['BAIRRO'] = df['BAIRRO'].replace({
        '0': 'Rosarinho',
        'POCO DA PANELA': 'POCO',
        'Rosarinho': 'ROSARINHO',
        'JOANA BEZERRA': 'ILHA JOANA BEZERRA',
        'BAIRRO DO RECIFE': 'RECIFE',
        'ALTO SANTA TERESINHA': 'ALTO SANTA TEREZINHA',
        'Afogados': 'AFOGADOS',
        'ARURDA': 'ARRUDA',
        'SAO JOSÊ': 'SAO JOSE'
    })

    mapa_rpa_para_regiao = {
    1: 'CENTRO',
    2: 'NORTE',
    3: 'NOROESTE',    # exemplo para o RPA 3
    4: 'OESTE',
    5: 'SUDESTE',
    6: 'SUL'
    # coloque todos os RPAs que conhece aqui
    }

    #df.fillna('não informado', inplace=True)
    df['REGIÃO'] = df['REGIÃO'].fillna(df['RPA'].map(mapa_rpa_para_regiao))
    return df

df = limpar_dados(df)

# Calculo da quantidade de pontos de wifi
totalWifi = df['NOME'].count()
totalBairro = df['BAIRRO'].count()

# criar o df para zonas e bairros
df_zona = df.groupby('REGIÃO')[['BAIRRO']].count().reset_index()
df_bairro = df.groupby('BAIRRO').size().reset_index(name='TOTAL').sort_values(by='TOTAL', ascending=False)
df_mapa = df[['BAIRRO', 'LATITUDE', 'LONGITUDE' ]]
