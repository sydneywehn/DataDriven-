import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
from datetime import date

def cur_day_injuries():

    injuries_page = requests.get(f'https://www.cbssports.com/nba/injuries/')
    injuries_page = BeautifulSoup(injuries_page.text, 'html.parser')

    team_count = {}

    injuries = []
    for team in injuries_page.find('main').find_all('div', {'class': 'TableBaseWrapper'}):
        t_name = team.find('span').find('a').getText()


        for stat in team.find('tbody').find_all('tr'):
            if t_name in team_count.keys():
                team_count[t_name] += 1
            else:
                team_count[t_name] = 1
            stats = stat.getText().strip('').split('\n')
            status = stats[25].strip(' ')
            injury = stats[22].strip(' ')
            date = stats[18].strip(' ')
            position = stats[13].strip(' ')
            full_name = stats[8]
            abr_name = stats[3]
            injuries.append([full_name, position, date, injury, status])

    players = []
    positions = []
    dates = []
    injury = []
    notes = []


    for p in injuries:
        #print(p)
        players.append(p[0])
        positions.append(p[1])
        dates.append(p[2])
        injury.append(p[3])
        notes.append(p[4])


    #print(injuries)
    #print(team_count)

    teams = []

    for team, count in team_count.items():
        for t in range(count):
            teams.append(team)

    df = pd.DataFrame()
    df['player'] = players
    df['position'] = positions
    df['date'] = dates
    df['injury'] = injury
    df['notes'] = notes

    df['team'] = teams
    return df



print(cur_day_injuries())