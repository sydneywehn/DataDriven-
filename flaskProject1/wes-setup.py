from db import execute_list_query, read_query, execute_query
import mysql.connector
from mysql.connector import Error
import pandas as pd


#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
# cnxn.close()
# cnxn = cnxn.cursor()


# Confirm connection worked
# q1 = """
# SELECT * FROM nba_game_data;
# """
#
# # q2 = """
# # DROP TABLE betting_lines;
# # """
# print(execute_query(cnxn, q1))

## Data manipulation
#


# Query NBA Game Data to get dataset
q1 = """
SELECT * FROM nba_game_data;
"""

nba_game_data = read_query(cnxn, q1)
#print(nba_game_data)
cols = box_stats = ['id', 'gid', 'team', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct', 'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'off_rtg', 'def_rtg', 'pts', 'date']
ngd_df = pd.DataFrame(nba_game_data, columns=cols)

#print(ngd_df.head())

# Query or use csv of line data
q2 = """
SELECT * FROM betting_lines;
"""

betting_lines = read_query(cnxn, q2)
#print(betting_lines)
bl_df = pd.DataFrame(betting_lines, columns=['id', 'h_team', 'a_team', 'open_spread', 'close_spread', 'open_total', 'close_total', 'home_ml', 'away_ml', 'home_score', 'away_score', 'date'])
#print(bl_df.head())

# Join datasets on
# home team + away team +  home points + away points
# (could make this a key potentially to avoid this join in the future)



# Run analysis on the data
