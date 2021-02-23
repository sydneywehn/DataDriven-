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


# Confirm connection worked
# q1 = """
# SELECT * FROM nba_game_data;
# """
#
# # q2 = """
# # DROP TABLE betting_lines;
# # """
# print(execute_query(cnxn, q1))


# Query NBA Game Data to get dataset
q1 = """
SELECT * FROM nba_game_data;
"""

#nba_game_data = execute_query(cnxn, q1)


# Query or use csv of line data
q2 = """
SELECT * FROM betting_lines;
"""

betting_lines = execute_query(cnxn, q2)
bl_df = pd.DataFrame(betting_lines,columns=['h_team', 'a_team', 'open_spread', 'close_spread', 'open_total', 'close_total', 'home_ml', 'away_ml', 'home_score', 'away_score', 'date'])
print(bl_df.head())

# Join datasets on home team + away team +  home points + away points (could make this a key potentially to avoid this join in the future)

# Run analysis on the data
