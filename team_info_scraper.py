import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from bs4 import BeautifulSoup

def foot_stat_scraper(file_name):

    with open(file_name) as page:
        soup = BeautifulSoup(page, "html.parser")
        soup = soup.find('tbody')
    
    pl_num = soup.find_all('div', {'class': 'rn_nummer'})
    pl_num_list = []
    for i in pl_num:
        pl_num_list.append(i.text)

    pl_name = soup.find_all('td', {'class': 'hide'})
    pl_name_list = []
    for i in pl_name:
        pl_name_list.append(i.text)

    pl_birth = soup.find_all('td', {'class': 'zentriert'})
    pl_birth_list = []
    for i in pl_birth:
        pl_birth_list.append(i.text)

    for i in pl_birth_list:
        if len(i) < 10:
            pl_birth_list.remove(i)
    for i in pl_birth_list:
        if len(i) < 10:
            pl_birth_list.remove(i)

    pl_price = soup.find_all('td', {'class': 'rechts'})
    pl_price_list = []
    for i in pl_price:
        pl_price_list.append(i.text)

    age_list = []
    for key, val in enumerate(pl_birth_list):
        age_list.append(val[-3:-1])
        pl_birth_list[key] = val[0:-5]

    pl_name_series = Series(pl_name_list)
    pl_num_series = Series(pl_num_list)
    pl_birth_series = Series(pl_birth_list) 
    pl_price_series = Series(pl_price_list) 
    pl_age_series = Series(age_list)
    pl_birth_series = pd.to_datetime(pd.Series(pl_birth_series))

    for key, price in enumerate(pl_price_series):
        price = price.replace('m', '0000')
        price = price.replace('.', '')
        price = price.replace('k', '000')
        price = price.replace('€', '')
        pl_price_series[key] = price

    team_info = pd.concat([pl_name_series, pl_num_series, pl_birth_series, pl_age_series, pl_price_series], axis=1)
    team_info.columns = ['Name', 'Number', 'Birth Date', 'Age', 'Price']
    team_info['Age'] = team_info['Age'].astype(int)
    team_info['Price'] = team_info['Price'].astype(int)
    return team_info

teams_list = ['Juve.html', 'inter.html']
seria_a_df = pd.DataFrame()
for team in teams_list:
    df = pd.DataFrame(foot_stat_scraper(str(team)))
    df['Team'] = team[0:-5]

    seria_a_df = seria_a_df.append(df, ignore_index=True)

#
print (seria_a_df)