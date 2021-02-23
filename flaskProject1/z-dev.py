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




def get_matchup_df():
    # Query DB
    q_home = 'SELECT G.pts, G.gid, M.date, M.home_team FROM nba_game_data G, nba_matchup M WHERE M.home_team=G.tid AND G.gid=M.gid AND M.date=G.date;'
    home_list = read_query(cnxn, q_home)

    q_away = home = 'SELECT G.pts, G.gid, M.away_team FROM nba_game_data G, nba_matchup M WHERE M.away_team=G.tid AND G.gid=M.gid AND M.date=G.date;'
    away_list = read_query(cnxn, q_away)

    # Put results in List
    all_home_pts = []
    all_gid = []
    all_date = []
    home_teams = []
    for pts, gid, date, home_team in home_list:
        all_home_pts.append(pts)
        all_gid.append(gid)
        all_date.append(date)
        home_teams.append(home_team)

    away_pts = []
    away_gid = []
    away_teams = []

    for pts, gid, away_team in away_list:
        away_pts.append(pts)
        away_gid.append(gid)
        away_teams.append(away_team)

    # Put list in pandas
    df_h = pd.DataFrame(list(zip(all_home_pts, all_gid, all_date, home_teams)),
                   columns =['h_pts', 'gid', 'date', 'h_team'])
    df_a = pd.DataFrame(list(zip(away_pts, away_gid, away_teams)),
                   columns =['a_pts', 'gid', 'a_team'])
    df_c = df_h.merge(df_a, on='gid')
    del df_c['gid']
    return df_c
df_c = get_matchup_df()





