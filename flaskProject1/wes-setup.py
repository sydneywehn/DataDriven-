from db import execute_list_query, read_query
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
q1 = """
SELECT * FROM nba_game_data;
"""
print(read_query(cnxn, q1))


# Query NBA Game Data to get dataset

# Query or use csv of line data

# Join datasets

# Run analysis on the data
