import numpy as np
import pandas as pd

import mlb
import nba
import nfl
import nhl

mlb_df = mlb.get_mlb_data()
nhl_df = nhl.get_nhl_data()
nba_df = nba.get_nba_data()
nfl_df = nfl.get_nfl_data()
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]


def sports_team_performance():


    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k: np.nan for k in sports}, index=sports)

    return p_values


print(mlb_df)
