import pandas as pd
from db import execute_list_query, read_query
import mysql.connector
from mysql.connector import Error
import itertools


#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)



# Process raw data from sportsbook review

#print(df.head())

def clean_sbr_data():
    df = pd.read_csv('nba odds 2020-21.csv')

    open_total = []
    close_total = []
    open_spread = []
    close_spread = []

    date = []
    v_team = []
    v_score = []
    v_ml = []

    h_team = []
    h_score = []
    h_ml = []

    for row in df.iterrows():
        data_row = row[1].values.flatten().tolist()
        # print(data_row[9])
        # print(type(data_row[9]))
        # Open
        if data_row[9] == 'pk':
            open_spread.append(data_row[9])
        elif float(data_row[9]) > 80:
            open_total.append(data_row[9])
        else:
            open_spread.append(data_row[9])

        # Close
        if data_row[10] == 'pk':
            close_spread.append(data_row[10])
        elif float(data_row[10]) > 80:
            close_total.append(data_row[10])
        else:
            close_spread.append(data_row[10])

        if data_row[2] == 'V':
            v_team.append(data_row[3])
            v_score.append(data_row[8])
            # only append date once
            date.append(data_row[0])
            v_ml.append(data_row[11])

        else:
            h_team.append(data_row[3])
            h_score.append(data_row[8])
            h_ml.append(data_row[11])

    #print(len(h_team), len(open_spread), len(close_spread), len(open_total), len(close_spread), len(date))

    final_df = pd.DataFrame()
    final_df['h_team'] = h_team
    final_df['h_score'] = h_score
    final_df['h_ml'] = h_ml
    final_df['a_team'] = v_team
    final_df['a_score'] = v_score
    final_df['a_ml'] = v_ml
    final_df['open_total'] = open_total
    final_df['close_total'] = close_total
    final_df['open_spread'] = open_spread
    final_df['close_spread'] = close_spread
    final_df['date'] = date

    #print(final_df.head())
    return final_df

# print(clean_sbr_data().head())

def insert_sbr_data():

    try:
        # Insert Query
        insert_into_bl = '''
                INSERT INTO betting_lines (home_team, home_score, home_ml, away_team, away_score, away_ml, open_total, close_total, open_spread, close_spread, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
            # Insert into db
        for row in clean_sbr_data().iterrows():
            #print(row)
            val = list(row[1].values)
            #print(val)
            vals = [(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10])]
            #print(vals)
            execute_list_query(cnxn, insert_into_bl, vals)
        return "Success"

    except:
        return "Something did not work"





