############# app.py ###############
# Point: All database commands
### Helper Functions:
# execute_query(connection, query) - delete or insert singular values
# read_query(connection, query) - select
# execute_list_query(connection, sql, val) - delete or insert as a list

### Database Commands
# Create Tables: nba_teams, nba_matchup, betting_lines, nba_game_data
# Insert: nba_teams, nba_game_data
####################################


import mysql.connector
from mysql.connector import Error
from sports_ref_scraper import get_team_game_data, get_df_matchups

#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)

#### BASIC QUERY FUNCTIONS

# Execute something like a delete or insert
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# Read query, something like a select
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        result = cursor.fetchall()

        return result, row_headers
    except Error as err:
        print(f"Error: '{err}'")

# Execute over a list, something with multiple values like inserting multiple values
def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

#### CREATING TABLE
# CREATE TABLES
create_nba_teams_table = """
CREATE TABLE nba_teams (
    tid VARCHAR(5),
    team_name VARCHAR(20),
    city VARCHAR(20),
    PRIMARY KEY (tid)
    );
"""

create_nba_matchup_table = """
CREATE TABLE nba_matchup (
    matchup_id INT NOT NULL AUTO_INCREMENT,
    home_team VARCHAR(5),
    away_team VARCHAR(5),
    gid VARCHAR(50),
    date INT NOT NULL,
    PRIMARY KEY (matchup_id)
);
"""

create_nba_game_data_table = """
CREATE TABLE nba_game_data (
    team_game_id INT NOT NULL AUTO_INCREMENT,
    gid VARCHAR(50),
    tid VARCHAR(5),
    fg INT,
    fga INT,
    fg_pct FLOAT,
    fg3 INT,
    fg3a INT,
    fg3_pct FLOAT,
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
    ts_pct FLOAT,
    efg_pct FLOAT,
    fg3a_per_fga_pct FLOAT,
    fta_per_fga_pct FLOAT,
    orb_pct FLOAT,
    drb_pct FLOAT,
    trb_pct FLOAT,
    ast_pct FLOAT,
    stl_pct FLOAT,
    blk_pct FLOAT,
    tov_pct FLOAT,
    off_rtg FLOAT,
    def_rtg FLOAT,
    date INT NOT NULL,
    PRIMARY KEY (team_game_id)
);

"""


create_betting_lines_table = """
CREATE TABLE betting_lines (
    bid INT NOT NULL AUTO_INCREMENT,
    home_team VARCHAR(50),
    away_team VARCHAR(50),
    open_spread INT,
    close_spread INT,
    open_total INT,
    close_total INT,
    home_ml INT,
    away_ml INT,
    home_score INT,
    away_score INT,
    date INT NOT NULL,
    PRIMARY KEY (bid)
);
"""



def execute_insert():
    execute_query(cnxn, create_nba_teams_table)
    execute_query(cnxn, create_nba_matchup_table)
    execute_query(cnxn, create_betting_lines_table)
    pass

#print(execute_insert())

### INSERT INTO TEAMS TABLE (tid = tor, name = Raptors, city = Toronto)

# Data
teams = [['Toronto', 'Raptors', 'TOR'],
         ['Boston', 'Celtics', 'BOS'],
         ['Philadelphia', '76ers', 'PHI'],
         ['Cleveland', 'Cavaliers', 'CLE'],
         ['Indiana', 'Pacers', 'IND]'],
         ['Miami', 'Heat', 'MIA'],
         ['Milwaukee', 'Bucks', 'MIL'],
         ['Washington', 'Wizards', 'WAS'],
         ['Detroit', 'Pistons', 'DET'],
         ['Charlotte', 'Hornets', 'CHO'],
         ['New York', 'Knicks', 'NYK'],
         ['Brooklyn', 'Nets', 'BRK'],
         ['Chicago', 'Bulls', 'CHI'],
         ['Orlando', 'Magic', 'ORL'],
         ['Atlanta', 'Hawks', 'ATL'],
         ['Houston', 'Rockets', 'HOU'],
         ['Golden State', 'Warriors', 'GSW'],
         ['Portland', 'Trail Blazers', 'POR'],
         ['Oklahoma City', 'Thunder', 'OKC'],
         ['Utah', 'Jazz', 'UTA'],
         ['New Orleans', 'Pelicans', 'NOP'],
         ['San Antonio', 'Spurs', 'SAS'],
         ['Minnesota', 'Timberwolves', 'MIN'],
         ['Denver', 'Nuggets', 'DEN'],
         ['Los Angeles', 'Clippers', 'LAC'],
         ['Los Angeles', 'Lakers', 'LAL'],
         ['Sacramento', 'Kings', 'SAC'],
         ['Dallas', 'Mavericks', 'DAL'],
         ['Memphis', 'Grizzlies', 'MEM'],
         ['Phoenix', 'Suns', 'PHO']]

# Insert Query
def insert_teams_data(cnxn, teams):
    insert_into_teams = '''
        INSERT INTO nba_teams (tid, team_name, city)
        VALUES (%s, %s, %s)
        '''
    # Insert into db
    for team in teams:
        val = [(team[2], team[1], team[0])]
        execute_list_query(cnxn, insert_into_teams, val)

# Insert all game data (call function not import df
def insert_all_game_data(connection):
    ### INSERT PANDAS INTO SQL for NBA GAME DATA TABLE

    # Insert Query
    insert_into_teams = '''
        INSERT INTO nba_game_data (gid, tid, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, 
        trb, ast, stl, blk, tov, pf, pts, ts_pct, efg_pct, fg3a_per_fga_pct, fta_per_fga_pct, orb_pct,
        drb_pct, trb_pct, ast_pct, stl_pct, blk_pct, tov_pct, off_rtg, def_rtg, date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
    # Insert into db
    for row in get_team_game_data().iterrows():
        val = list(row[1].values)
        vals = [(val[31], val[32], val[0], val[1], float(val[2]), val[3], val[4], float(val[5]), val[6], val[7],
                 float(val[8]), val[9], val[10], val[11], val[12], val[13], val[14], val[15], val[16], float(val[17]),
                 float(val[18]), float(val[19]), float(val[20]), float(val[21]), float(val[22]), float(val[23]),
                 float(val[24]), float(val[25]), float(val[26]), float(val[27]), float(val[28]), float(val[29]),
                 float(val[30]), val[33])]
        execute_list_query(connection, insert_into_teams, vals)
    return "All game data inserted"

def insert_game_matchups(cnxn):
    # Insert Query
    insert_into_teams = '''
        INSERT INTO nba_matchup (home_team, away_team, gid, date) 
        VALUES (%s, %s, %s, %s)
        '''
    # Insert into db
    for row in get_df_matchups().iterrows():
        val = list(row[1].values)
        vals = [(val[0], val[1], val[2], val[3])]
        execute_list_query(cnxn, insert_into_teams, vals)
    return "Game matchups inserted"

# print(insert_all_game_data(cnxn))
# print(insert_game_matchups(cnxn))

# # Confirm it actually worked
# q1 = """
# SELECT * FROM nba_game_data;
# """
# print(read_query(cnxn, q1))
# def test():
#     return read_query(cnxn, q1)