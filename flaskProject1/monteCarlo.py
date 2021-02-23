import mysql.connector
from mysql.connector import Error
import pandas as pd
from itertools import *
import datetime
from db import execute_list_query, read_query

#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)




# Make the Monte Carlo df
#
# # Confirm it actually worked
# team_abr = {'Toronto': 'TOR',
#             'Boston': 'BOS',
#             'Philadelphia': 'PHI',
#             'Cleveland': 'CLE',
#             'Indiana': 'IND',
#             'Miami': 'MIA',
#             'Milwaukee': 'MIL',
#             'Washington': 'WAS',
#             'Detroit': 'DET',
#             'Charlotte': 'CHO',
#             'New York': 'NYK',
#             'Brooklyn': 'BRK',
#             'Chicago': 'CHI',
#             'Orlando': 'ORL',
#             'Atlanta': 'ATL',
#             'Houston': 'HOU',
#             'Golden State': 'GSW',
#             'Portland': 'POR',
#             'Oklahoma City': 'OKC',
#             'Utah': 'UTA',
#             'New Orleans': 'NOP',
#             'San Antonio': 'SAS',
#             'Minnesota': 'MIN',
#             'Denver': 'DEN',
#             'L.A. Clippers': 'LAC',
#             'L.A. Lakers': 'LAL',
#             'Sacramento': 'SAC',
#             'Dallas': 'DAL',
#             'Memphis': 'MEM',
#             'Phoenix': 'PHO'}
#
# def query_team(tid):
#     q1 = "SELECT tid, avg(pts) FROM nba_game_data WHERE tid='{}' AND date>20201210;".format(tid)
#     return q1
#
#
# opp_points = []
# avgs = []
# team_avg_points = []
# for team in team_abr.values():
#     games_query = "SELECT gid FROM nba_game_data WHERE tid='{}' AND date>20201210;".format(team.lower())
#     all_games = read_query(cnxn, games_query)
#     for game in all_games:
#         gid = game[0]
#         query2 = "SELECT pts FROM nba_game_data WHERE tid!='{}' AND gid='{}' AND date>20201210".format(team.lower(),
#                                                                                                        gid)
#         opp_points.append(read_query(cnxn, query2))
#     avg = []
#     for opp in opp_points:
#         avg.append(opp[0][0])
#
#     df = pd.DataFrame(avg)
#
#     avgs.append(df.mean())
#
#     avg = []
#     opp_points = []
#     del df
#
#     q = query_team(team.lower())
#     team_avg_points.append(read_query(cnxn, q))
#
# team_avg_op_points = []
# for x in avgs:
#     team_avg_op_points.append(x.values[0])
#
# # print(team_avg_points, team_avg_op_points)
# teams = []
# pts = []
# op_pts = []
# for t, op in zip(team_avg_points, team_avg_op_points):
#     teams.append(t[0][0])
#     pts.append(t[0][1])
#     op_pts.append(op)
#
# final_df = pd.DataFrame(teams)
# final_df['avg_pts'] = pts
# final_df['op_avg_pts'] = op_pts


# INPUT: csv_file name as str, df that needs saved
#
def save_df(csv_name, df):
    compression_opts = dict(method='zip',
                        archive_name=csv_name+'.csv')

    df.to_csv(csv_name+'.zip', index=False, compression=compression_opts)
    return 'Saved'

#print(final_df.head())
#save_df('monteCarlo', final_df)
## FULLONE

# Confirm it actually worked
team_abr = {'Toronto': 'TOR',
            'Boston': 'BOS',
            'Philadelphia': 'PHI',
            'Cleveland': 'CLE',
            'Indiana': 'IND',
            'Miami': 'MIA',
            'Milwaukee': 'MIL',
            'Washington': 'WAS',
            'Detroit': 'DET',
            'Charlotte': 'CHO',
            'New York': 'NYK',
            'Brooklyn': 'BRK',
            'Chicago': 'CHI',
            'Orlando': 'ORL',
            'Atlanta': 'ATL',
            'Houston': 'HOU',
            'Golden State': 'GSW',
            'Portland': 'POR',
            'Oklahoma City': 'OKC',
            'Utah': 'UTA',
            'New Orleans': 'NOP',
            'San Antonio': 'SAS',
            'Minnesota': 'MIN',
            'Denver': 'DEN',
            'L.A. Clippers': 'LAC',
            'L.A. Lakers': 'LAL',
            'Sacramento': 'SAC',
            'Dallas': 'DAL',
            'Memphis': 'MEM',
            'Phoenix': 'PHO'}


def query_team(tid):
    q1 = "SELECT tid, pts FROM nba_game_data WHERE tid='{}' AND date>20201210;".format(tid)
    return q1


opp_points = []
team_points = []
for team in team_abr.values():
    games_query = "SELECT gid FROM nba_game_data WHERE tid='{}' AND date>20201210;".format(team.lower())
    all_games = read_query(cnxn, games_query)
    for game in all_games:
        gid = game[0]
        query2 = "SELECT pts FROM nba_game_data WHERE tid!='{}' AND gid='{}' AND date>20201210".format(team.lower(),
                                                                                                       gid)
        opp_points.append(read_query(cnxn, query2))
    avg = []
    for opp in opp_points:
        avg.append(opp[0][0])

    q = query_team(team.lower())
    team_points.append(read_query(cnxn, q))

team = []
all_team_points = []

for x in team_points:
    for t in x:
        team.append(t[0])
        all_team_points.append(t[1])

opp_points_cleaned = []
for op in opp_points:
    opp_points_cleaned.append(op[0][0])

print(len(team), len(all_team_points), len(opp_points_cleaned))


syds_monte = pd.DataFrame(team)
syds_monte['team_points'] = all_team_points
syds_monte['opp_points'] = opp_points_cleaned

save_df('full_monte', syds_monte)

