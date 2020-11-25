import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def clear_data(string1):
    if re.search(r'\[[a-z]* [0-9]+\]', string1) is None:
        return string1
    else:
        return string1.replace(re.search(r'\[[a-z]* [0-9]+\]', string1).group(), '')


def clear_nba_data(string1):
    if re.search(r'\*|\+', string1) is None:
        return string1
    else:
        return string1.replace(re.search(r'\*|\+', string1).group(), '')


def get_area(team):
    for each in list(nfl_cities.index.values):
        if team in each:
            return nfl_cities.at[each, 'Metropolitan area']


population_by_region = []  # pass in metropolitan area population from cities
win_loss_by_region = []  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
nfl_df = pd.read_csv("assets/nfl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1,[0,3,5,6,7,8]]
nfl_df = nfl_df[nfl_df['year'] == 2018].drop([0, 5, 10, 15, 20, 25, 30, 35])  # get only 2018 stats
population = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
population = population.set_index('Metropolitan area')
cities['NFL'] = cities['NFL'].apply(lambda x: clear_data(x))
nfl_cities = cities[['Metropolitan area', 'NFL']].set_index('NFL')
nfl_cities = nfl_cities.drop(['—', ''], axis=0)
nfl_df['team'] = nfl_df['team'].apply(lambda x: clear_nba_data(x))
nfl_df['area'] = nfl_df['team'].apply(lambda x: x.split(" ")[-1])
nfl_df['area'] = nfl_df['area'].apply(lambda x: get_area(x))
out = []
for group, frame in nfl_df.groupby('area'):
    total_wins = int(np.sum(frame['W']))
    total_matches = int(np.sum(frame['L'])) + int(np.sum(frame['W']))
    ratio = total_wins / total_matches
    out_dict = {
        'Area': group,
        'Ratio': ratio
    }
    out.append(out_dict)
new_df = pd.DataFrame(out)
new_df = new_df.set_index('Area')
out_df = pd.merge(new_df, population, how="inner", left_index=True, right_index=True)
out_df['Population (2016 est.)[8]'] = pd.to_numeric(out_df['Population (2016 est.)[8]'])
population_by_region = out_df['Population (2016 est.)[8]'].to_list()
win_loss_by_region = out_df['Ratio'].to_list()
print(stats.pearsonr(population_by_region, win_loss_by_region))
