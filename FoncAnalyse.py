from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

ticker = "AMZN"
end_date = datetime.now()
start_date = end_date-timedelta(days=600)

historical_prices = si.get_data(ticker, start_date=start_date, end_date=end_date)
df = historical_prices

ma80 = df['close'].rolling(80).mean()

top5TradableStocks = si.get_day_most_active().head()["Symbol"]


###------ Fonction ------###

# Donne la tendance de fond
def tendancesDeF(ticker):
    if ma80.iloc[-1] > si.get_live_price(ticker):
        return ":arrow_lower_right:"
    else :
        return ":arrow_upper_right:"

# Indique si Oui ou Non il faut trader ce stock en ce moment
def Tradable(myTicker):
    for symbol in si.get_day_most_active()["Symbol"]:
        if symbol == myTicker.upper():
            return ":white_check_mark:"
    return ":no_entry:"

## Scrapping du dataframe pour le Calendrier économique ##

def scrapCalEco():
    # URL de la page à récupérer
    url = 'https://www.investing.com/economic-calendar/'

    # Effectuer une requête GET
    response = requests.get(url)

    # Créer un objet BeautifulSoup à partir de la réponse
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver la table avec l'ID "economicCalendarData"
    table = soup.find('table', {'id': 'economicCalendarData'})

    # Extraire les noms de colonnes depuis le premier <thead>
    thead = table.find_all('thead')[0]
    cols = [col.get_text().strip() for col in thead.find_all('th')]

    # Créer une liste vide pour stocker les données
    data = []

    # Extraire les données depuis la deuxième <tbody>
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        # Extraire les colonnes de chaque ligne
        cols_row = [col.get_text().strip() for col in row.find_all('td')]
        
        # Mettre à jour la colonne "Importance" en fonction de la valeur de l'attribut "title" de chaque élément "td"
        for i, col in enumerate(row.find_all('td')):
            if 'High Volatility Expected' in col.get('title', ''):
                cols_row[i] = 'Fort'
            elif 'Moderate Volatility Expected' in col.get('title', ''):
                cols_row[i] = 'Moyen'
            elif 'Low Volatility Expected' in col.get('title', ''):
                cols_row[i] = 'Faible'

        # Supprimer la première colonne correspondant à la date du jour
        cols_row.pop(0)
        # Ajouter les colonnes à la liste de données
        data.append(cols_row)



    # Créer un DataFrame pandas à partir des données et des noms de colonnes
    df = pd.DataFrame(data, columns=cols[1:])
    df = df.iloc[1:]
    df = df.drop('', axis=1)
    df.iloc[:, 0:1] = df.iloc[:, 0:1].where(df.iloc[:, 0:1].apply(lambda x: x.str.strip() != ''), other=np.nan)
    df.iloc[:, 3:] = df.iloc[:, 3:].where(df.iloc[:, 3:].apply(lambda x: x.str.strip() != ''), other=np.nan)
    df = df.rename(columns={'Cur.': 'Currency', 'Imp.': 'Importance'})
    df.dropna(subset=["Currency"], inplace=True)
    df = df.reset_index(drop=True)


    # Afficher le contenu du premier <td> avec la classe "theDay"
    DateDuCalendrier = soup.find_all('td', {'class': 'theDay'})[0].get_text().strip()

    # Afficher le DataFrame
    return df, DateDuCalendrier