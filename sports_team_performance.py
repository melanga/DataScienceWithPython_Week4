import numpy as np
import pandas as pd
import scipy.stats as stats

import mlb
import nba
import nfl
import nhl

MLB = mlb.get_mlb_data().drop('Population (2016 est.)[8]', axis=1)
NHL = nhl.get_nhl_data().drop('Population (2016 est.)[8]', axis=1)
NBA = nba.get_nba_data().drop('Population (2016 est.)[8]', axis=1)
NFL = nfl.get_nfl_data().drop('Population (2016 est.)[8]', axis=1)
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
data_set = {'NFL': NFL,
            'NBA': NBA,
            'NHL': NHL,
            'MLB': MLB}


def get_p_value(k):
    p_values = []
    for each in data_set:
        df = pd.merge(data_set[k], data_set[each], how="inner", left_index=True, right_index=True)
        nhl_corr = stats.ttest_rel(df['Ratio_x'], df['Ratio_y'])[1]
        nhl_corr = round(nhl_corr, 2)
        p_values.append(nhl_corr)
    return p_values


def sports_team_performance():
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k: get_p_value(k) for k in sports}, index=sports)
    return p_values


print(sports_team_performance())
