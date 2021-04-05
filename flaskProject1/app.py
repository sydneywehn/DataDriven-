############# app.py ###############
# Point: Controls the api, calls all other functions and sends data

### Functions:
# injuries() - call nba_injuries_scraper
####################################




from flask import Flask, jsonify
from db import execute_list_query, read_query
from nba_injuries_scraper import cur_day_injuries
import mysql.connector
import json
from mysql.connector import Error


#### CONNECT TO GOOGLE CLOUD MYSQL
config = {
    'user': 'root',
    'password': 'txybkx5kPMpko8C6',
    'host': '35.238.14.103'
}
config['database'] = 'ddx_db'  # add new database to config dict
cnxn = mysql.connector.connect(**config)

app = Flask(__name__)


# Test rn, showing concept
@app.route('/')
def hello_world():
    # Query NBA Game Data to get dataset
    q1 = """
    SELECT pts FROM nba_game_data;
    """
    rv, row_headers = read_query(cnxn, q1)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)

# Returns injuries as json (scrapes CBS site from function)
# Need to add: parameters to query by team
@app.route('/injuries')
def injuries():
    irs = cur_day_injuries()
    return irs

# Betting Lines (total, spread, money line) for each team (highlight what bet hit), Points for each team
@app.route('/last_ten')
def nba_last_ten_games():
    pass


# Home team away team Betting lines (total, spread, money line)
@app.route('/cur_day_matchups')
def nba_cur_day_matchups():
    pass

# monte carlo (ml, spread, total)
@app.route('/nba_predict')
def nba_predict():
    pass

# summary stats (ATS Record, O/U record, Overall Record,  Off/ Def Rtg, Avg points per game)
@app.route('sum_stats')
def nba_sum_stats():
    pass

# player overview table
# Stats: Player average stats (average points, assist, rebounds)
@app.route('/player_avg')
def nba_player_avg():
    pass


# https://newsapi.org/s/us-sports-news-api
@app.route('/news')
def news_api():
    pass


if __name__ == '__main__':
    app.run()
