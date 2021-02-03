import pandas as pd
from itertools import *
import itertools
import datetime
from datetime import date
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from db import execute_list_query, read_query
import mysql.connector
from mysql.connector import Error


#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)


team_handles = {'Toronto Raptors': 'TOR',
                     'Boston Celtics': 'BOS',
                     'Philadelphia 76ers': 'PHI',
                     'Cleveland Cavaliers': 'CLE',
                     'Indiana Pacers': 'IND',
                     'Miami Heat': 'MIA',
                     'Milwaukee Bucks': 'MIL',
                     'Washington Wizards': 'WAS',
                     'Detroit Pistons': 'DET',
                     'Charlotte Hornets': 'CHO',
                     'New York Knicks': 'NYK',
                     'Brooklyn Nets': 'BRK',
                     'Chicago Bulls': 'CHI',
                     'Orlando Magic': 'ORL',
                     'Atlanta Hawks': 'ATL',
                     'Houston Rockets': 'HOU',
                     'Golden State Warriors': 'GSW',
                     'Portland Trail Blazers': 'POR',
                     'Oklahoma City Thunder': 'OKC',
                     'Utah Jazz': 'UTA',
                     'New Orleans Pelicans': 'NOP',
                     'San Antonio Spurs': 'SAS',
                     'Minnesota Timberwolves': 'MIN',
                     'Denver Nuggets': 'DEN',
                     'Los Angeles Clippers': 'LAC',
                     'Los Angeles Lakers': 'LAL',
                     'Sacramento Kings': 'SAC',
                     'Dallas Mavericks': 'DAL',
                     'Memphis Grizzlies': 'MEM',
                     'Phoenix Suns': 'PHO'}

def cur_day_nba_matchups():

    soup = requests.get(f'https://www.basketball-reference.com/leagues/NBA_2021_games-february.html')
    soup = BeautifulSoup(soup.text, 'html.parser')
    matchup = []

    for row in soup.find('table', {'id': 'schedule'}).find_all('tr'):
        _class = row.get("class")

        # skip table body header
        if _class is not None:
            continue
        # above skip was not working
        if row.find('a') is not None:
            url_day = row.find('a')['href'].split('&')
            day = int(url_day[1].replace('day=', ''))
            cur_day = date.today().day
            if day == (cur_day):
                h_team = row.find_all('a')[1]
                a_team = row.find_all('a')[2]
                matchup.append((h_team.getText(), a_team.getText()))
                #print(h_team.getText())
                #print(a_team.getText())
                #print("----------")
                # insert data into SQL
                # will insert into game data by clicking on box score and will insert into matchup
    return matchup


# function to get box score stats of advanced and basic with gid=/boxscores/201903010ATL.html
def get_box_score_stats(gid):
    box_score_page = requests.get(f'https://www.basketball-reference.com/{gid}')
    box_score_page = BeautifulSoup(box_score_page.text, 'html.parser')
    bs_page_teams = []
    bs_page_score = []

    # get team names
    for item in box_score_page.find('div', attrs={'class', 'scorebox'}).find_all('strong'):
        team_slug = team_handles[item.text.replace('\n', '')]
        bs_page_teams.append(team_slug.lower())

    # get teams score
    for score in box_score_page.find('div', attrs={'class', 'scorebox'}).find_all('div', attrs={'class', 'score'}):
        bs_page_score.append(score.getText())

    box_score_data = []
    advanced_score_data = []
    tables = box_score_page.find_all("table")
    for i, table in enumerate(tables, start=1):
        for td in table.find_all('tfoot'):
            box_stats1 = ['mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb',
                          'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
            advanced_stats = ['ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct',
                              'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg']
            data = [[td1.getText() for td1 in td.findAll('td', {'data-stat': stat})] for stat in box_stats1]
            box_score_data.append(data)
            # print("basic",data)
            advanced_score = [[td2.getText() for td2 in td.findAll('td', {'data-stat': a_stat})] for a_stat in
                              advanced_stats]
            advanced_score_data.append(advanced_score)
            # print("advanced", advanced_score_data)

    # print(pd.DataFrame(advanced_score_data).head(50))
    # print(pd.DataFrame(box_score_data).head(50))

    advanced_score_df = pd.DataFrame(advanced_score_data)
    advanced_score_df = advanced_score_df.dropna(how='all')
    # print(advanced_score_df.head(10))

    return bs_page_teams, box_score_data, advanced_score_data, bs_page_score


#update_nba_games()

def update_nba_game_data_and_matchup():
    box_scores = []
    soup = requests.get('https://www.basketball-reference.com//boxscores/index.fcgi?month=2&day=1&year=2021')
    soup = BeautifulSoup(soup.text, 'html.parser')
    for row in soup.find('div', {'class': 'game_summaries'}).find_all('div'):
        box_scores.append(row.find('p').find('a')['href'])


    final_list_basic = []
    final_list_advanced = []
    ordered_teams = []
    ordered_scores = []
    for box in box_scores:
        teams, b_score_data, a_score_data, scores = get_box_score_stats(box)
        # order score data
        for score in scores:
            ordered_scores.append(score)

        # get the basic score data into dataframe ready format
        for b in b_score_data:
            if b[1] != []:
                final_list_basic.append(b)

        # get the teams in dataframe format
        for team in teams:
            ordered_teams.append(team)

        # finding data and appending to final_list of data (need to ignore empty columns) for advanced
        for a in a_score_data:
            if a[-1] != []:
                final_list_advanced.append(a)


    # combine everything

    advanced_stats_cols = ['ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct', 'trb_pct',
                           'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg']
    box_stats_cols = ['mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb',
                      'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
    combined_df = ['mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast',
                   'stl', 'blk', 'tov', 'pf', 'pts', 'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct',
                   'drb_pct', 'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg']

    # make dataframes have correct value type, removing the stupid [] from each number
    df = pd.DataFrame(final_list_basic)
    for i in range(0, 19):
        df[i] = df[i].str[0]

    df1 = pd.DataFrame(final_list_advanced)
    for i in range(0, 14):
        df1[i] = df1[i].str[0]

    # iterating through to get them in the same pick
    df.columns = box_stats_cols

    df_full_game = df.loc[(pd.to_numeric(df['mp']) >= 240)]

    new_list = []
    # Iterate through the two dataframes at once to have each game at that place and append all game stats to that new list
    for b, a in itertools.zip_longest(df_full_game.iterrows(), df1.iterrows()):
        basic = list(b[1].values)
        advance = list(a[1].values)
        combined = basic + advance
        new_list.append(combined)

    new_df = pd.DataFrame(new_list)
    new_df.columns = combined_df

    # print(df.head())
    # print(len(df_full_game))
    df1.columns = advanced_stats_cols


    all_box_scores = []
    for box_score in box_scores:
        all_box_scores.append(box_score)
        all_box_scores.append(box_score)

    cur_day = str(date.today()).replace('-', '')
    pre_day = int(cur_day)-1
    print(pre_day)
    df_dates = []
    for d in all_box_scores:
        df_dates.append(pre_day)

    new_df['gid'] = all_box_scores
    new_df['team'] = ordered_teams
    new_df['date'] = df_dates

    del new_df['mp']
    del new_df['usg_pct']

    print(new_df.head())

    ## GET THE MATCHUP DATA
    print(len(df1), len(df_dates))
    df1['team'] = ordered_teams
    df1['gid'] = all_box_scores
    df1['date'] = df_dates
    df_join = df1.join(df1.shift(-1).add_prefix('away_'))
    df_join[1::2] = ''
    df_join = df_join[df_join.ts_pct != '']

    df_matchups = df_join[['team', 'away_team', 'gid', 'date']]
    print(df_matchups.head())
    ### INSERT PANDAS INTO SQL for NBA GAME DATA TABLE

    # Insert Query
    insert_into_teams = '''
        INSERT INTO nba_game_data (gid, tid, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, 
        trb, ast, stl, blk, tov, pf, pts, ts_pct, efg_pct, fg3a_per_fga_pct, fta_per_fga_pct, orb_pct,
        drb_pct, trb_pct, ast_pct, stl_pct, blk_pct, tov_pct, off_rtg, def_rtg, date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
    # Insert into db
    for row in new_df.iterrows():
        val = list(row[1].values)
        vals = [(val[31], val[32], val[0], val[1], float(val[2]), val[3], val[4], float(val[5]), val[6], val[7],
                 float(val[8]), val[9], val[10], val[11], val[12], val[13], val[14], val[15], val[16], float(val[17]),
                 float(val[18]), float(val[19]), float(val[20]), float(val[21]), float(val[22]), float(val[23]),
                 float(val[24]), float(val[25]), float(val[26]), float(val[27]), float(val[28]), float(val[29]),
                 float(val[30]), val[33])]
        execute_list_query(cnxn, insert_into_teams, vals)
    # add insert command tomorrow for matchups


print(cur_day_nba_matchups())
# confirm it works
# #update_nba_game_data_and_matchup()
# q='SELECT * from nba_game_data WHERE date=20210201;'
# print(read_query(cnxn,q))