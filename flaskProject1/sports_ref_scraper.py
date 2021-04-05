############# sports_ref_scraper.py ###############
# Point: Scrape Sports Book Reference
### Functions:
# get_player_data() - get nba player data by player - not done, need to complete return
# scrape_nba_game_data(): - (has getters to get individual dataframes) - get matchups and all stats for 2021

####################################


import requests
from bs4 import BeautifulSoup
import pandas as pd
import itertools
import datetime
import os


############ HELPER FUNCTIONS ##################
# Input: list from query, col names
def list_to_df(ls, cols):
    return pd.DataFrame(ls, columns=cols)

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day



# Create Tables
create_nba_teams_table = """
CREATE TABLE nba_player_totals (
    pid INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100), 
    pos VARCHAR(5), 
    age INT,
    tid VARCHAR(5),
    gp INT,
    mp INT,
    fg INT,
    fga INT,
    fg_pct FLOAT,
    fg3 INT,
    fga3 INT,
    fg3_pct FLOAT,
    fg2 INT,
    fga2 INT,
    fg2_pct FLOAT,
    efg_pct FLOAT,
    ft INT,
    fta INT,
    ft_pct FLOAT,
    orb INT,
    drb INT,
    trb INT,
    ast INT,
    stl INT,
    blk INT,
    tov INT,
    pf INT,
    pts INT,    
    PRIMARY KEY (pid)
    );
"""


# Scrape player data from (click tabs for all the data):
# https://www.basketball-reference.com/leagues/NBA_2021_totals.html

# Totals, Per Game, Per 36 Min, Per 100 Poss have same columns
# Totals Url: https://www.basketball-reference.com/leagues/NBA_2021_totals.html
# Per Game: https://www.basketball-reference.com/leagues/NBA_2021_per_game.html
# have everything but adjusted shooting and shooting (can do shooting with what we have - zack is lazy)

def get_player_data():

    webpages = ['totals', 'per_game', 'per_minute', 'per_poss', 'advanced', 'play-by-play']

    for webpage in webpages:
        year = 2021
        soup = requests.get(f'https://www.basketball-reference.com/leagues/NBA_{year}_{webpage}.html')
        soup = BeautifulSoup(soup.text, 'html.parser')
        data = soup.find('table').find_all('tr')
        all_data = []
        for row in data:
            row_data = row.find_all('td')
            all_data.append([x.getText() for x in row_data])

        if webpage == 'totals' or webpage == 'per_game' or webpage == 'per_minute' or webpage == 'per_poss':
            # used for totals, per game, per 36 min, per 100 poss
            t_cols = ['name', 'pos', 'age', 'tid', 'gp', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fga3', 'fg3_pct', 'fg2',
                      'fga2', 'fg2_pct', 'efg_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov',
                      'pf', 'pts']
            list_to_df(all_data, t_cols)
        elif webpage == 'advanced':
            adv_cols = ['name', 'pos', 'age', 'tid', 'gp', 'mp', 'per', 'ts_pct', 'fga3_r', 'ft_r', 'orb_pct', 'drb_pct',
                        'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'ows', 'dws', 'ws', 'ws_48',
                        'obpm', 'dbpm', 'bpm', 'vorp']
            list_to_df(all_data, adv_cols)
        elif webpage == 'play-by-play':
            play_by_play_cols = ['name', 'pos', 'age', 'tid', 'gp', 'mp', 'pg_pct', 'sg_pct', 'pos_sf_pct', 'pos_pf_pct',
                            'pos_c_pct', 'per_100_on_court', 'per_100_on_off', 'tov_bad_pass', 'tov_lost_ball',
                            'foul_shoot', 'foul_off', 'foul_drawn_shoot', 'foul_drawn_off', 'pga', 'and1', 'blkd']
            list_to_df(all_data, play_by_play_cols)
    return "need to figure out return"



# 1. Scrape data
# 2. Drop old table
# 3. Create new table
# 4. Insert Data


##### Game data #######

# Funcitons
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


def get_game_info(team_handle, year):
    season_page = requests.get(f'https://www.basketball-reference.com/teams/{team_handle}/{year}_games.html')
    season_page = BeautifulSoup(season_page.text, 'html.parser')

    stats = ['date_game', 'game_start_time', 'network', 'opp_name', 'game_result', 'overtimes', 'pts', 'opp_pts',
             'wins', 'losses', 'game_streak']
    stats_list = [[td.getText() for td in season_page.findAll('td', {'data-stat': stat})] for stat in stats]

    box_scores = []
    dates = []

    for row in season_page.find('table', {'id': 'games'}).tbody.find_all('tr'):
        _class = row.get("class")

        # skip table body header
        if _class is not None and "thead" == _class[0]:
            continue

        game_result = row.find('td', {'data-stat': 'game_result'}).getText()

        # if there isnt a game result yet, the game has not played and we dont need that info
        if game_result == '':
            return stats_list, box_scores, dates

        # only get every teams home game so we do not have duplicates
        game_loc = row.find('td', {'data-stat': 'game_location'}).getText()
        if game_loc == '':
            box_score = row.find('td', {'data-stat': 'box_score_text'}).find('a')['href']
            box_scores.append(box_score)
            date = row.find('td', {'data-stat': 'date_game'})['csk']
            dates.append(date)

    return stats_list, box_scores, dates


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

# return full dataframe in three parts: df_matchups, new_df, df_join
def scrape_nba_game_data():
    all_dates = []
    all_box_scores = []
    for team in team_handles.values():
        stats_list, box_scores, dates = get_game_info(team, 2021)
        all_box_scores.append(box_scores)
        all_dates.append(dates)

    final_list_basic = []
    final_list_advanced = []
    ordered_teams = []
    ordered_scores = []
    for team_box_score in all_box_scores:
        for box_score in team_box_score:
            teams, b_score_data, a_score_data, scores = get_box_score_stats(box_score)

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

    print(len(ordered_scores), len(ordered_teams))

    # combine everything
    import itertools

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

    df_dates = []
    for date in all_dates:
        for d in date:
            # split datetime and convert to int
            dateSplit = d.split('-')
            d_append = to_integer(datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2])))

            # do 2x because each game has 2 rows, 1 for each team
            df_dates.append(d_append)
            df_dates.append(d_append)

    box_scores = []
    for box_score in all_box_scores:
        for box in box_score:
            box_scores.append(box)
            box_scores.append(box)

    new_df['gid'] = box_scores
    new_df['team'] = ordered_teams
    new_df['date'] = df_dates

    del new_df['mp']
    del new_df['usg_pct']

#print(new_df.head())

    ## GET THE MATCHUP DATA
    print(len(df1), len(df_dates))
    df1['team'] = ordered_teams
    df1['gid'] = box_scores
    df1['date'] = df_dates
    df_join = df1.join(df1.shift(-1).add_prefix('away_'))
    df_join[1::2] = ''
    df_join = df_join[df_join.ts_pct != '']

    df_matchups = df_join[['team', 'away_team', 'gid', 'date']]
    return df_matchups, new_df, df_join

# Set of getters to get specific dataframe
def get_df_matchups():
    df_matchups, new_df, df_join = scrape_nba_game_data()
    return df_matchups

def get_team_game_data():
    df_matchups, new_df, df_join = scrape_nba_game_data()
    return new_df

def get_matchup_stats():
    df_matchups, new_df, df_join = scrape_nba_game_data()
    return df_join




# print(get_df_matchups().columns)
# print(get_team_game_data().columns)





