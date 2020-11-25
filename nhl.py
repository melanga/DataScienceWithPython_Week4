import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def clear_data(string1):
    if re.search(r'\[[a-z]* [0-9]+\]', string1) is None:
        return string1
    else:
        return string1.replace(re.search(r'\[[a-z]* [0-9]+\]', string1).group(), '')


def get_area(team):
    for each in list(nhl_cities.index.values):
        if team in each:
            return nhl_cities.at[each, 'Metropolitan area']


def get_nhl_data():
    return out_df


population_by_region = []  # pass in metropolitan area population from cities
win_loss_by_region = []  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
nhl_df = pd.read_csv("assets/nhl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
nhl_df = nhl_df[nhl_df['year'] == 2018].drop([0, 9, 18, 26], axis=0) # get only 2018 stats
population = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
population = population.set_index('Metropolitan area')
cities['NHL'] = cities['NHL'].apply(lambda x: clear_data(x))
nhl_cities = cities[['Metropolitan area', 'NHL']].set_index('NHL')
nhl_cities = nhl_cities.drop(['—', ''], axis=0)
nhl_df['team'] = nhl_df['team'].apply(lambda x: x[:-1].strip() if x.endswith("*") else x.strip())
nhl_df['area'] = nhl_df['team'].apply(lambda x: x.split(" ")[-1])
nhl_df['area'] = nhl_df['area'].apply(lambda x: get_area(x))
print(nhl_df)
out = []
for group, frame in nhl_df.groupby('area'):
    total_wins = np.sum(pd.to_numeric(frame['W']))
    total_losses = np.sum(pd.to_numeric(frame['L']))
    total_matches = total_wins + total_losses
    ratio = (total_wins / total_matches)
    out_dict = {
        'Area': group,
        'Ratio': ratio
    }
    out.append(out_dict)
new_df = pd.DataFrame(out)
new_df = new_df.set_index('Area')
out_df = pd.merge(new_df, population, how="inner", left_index=True, right_index=True)
out_df['Population (2016 est.)[8]'] = pd.to_numeric(out_df['Population (2016 est.)[8]'])
population_by_region = out_df['Population (2016 est.)[8]']
win_loss_by_region = out_df['Ratio']
print(new_df)
print(stats.pearsonr(population_by_region, win_loss_by_region)[0])
