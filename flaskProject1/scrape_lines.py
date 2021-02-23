## GET SPORTSBOOK REVIEW DATA
import json
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import date









# OLD STUFF

# # get spreads
# def get_betting_spreads(date):
#     info_list = []
#     betting_page = requests.get(f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/?date={date}')
#     time.sleep(2)
#     betting_page = BeautifulSoup(betting_page.text, 'html.parser')
#     teams_list = []
#     for row in betting_page.find_all('div', {'class': 'eventLine-value'}):
#         teams_list.append(row.text)
#     betting_lines = []
#     for item in betting_page.find_all('div', {'class': 'event-holder holder-complete'}):
#         for line in item.find_all('div', {'class': 'el-div eventLine-book'}):
#             if line.text != '':
#                 betting_lines.append(line.text)
#                 break
#
#     betting_lines = [line.replace('\xa0', ' ') for line in betting_lines]
#     date_list = [date for item in betting_lines]
#     zipped_teams_lines = zip(date_list, teams_list, betting_lines)
#     return list(zipped_teams_lines)
#
#
# # Get betting line totals
# def get_betting_totals(date):
#     info_list = []
#     betting_page = requests.get(f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/totals/?date={date}')
#     time.sleep(2)
#     betting_page = BeautifulSoup(betting_page.text, 'html.parser')
#     teams_list = []
#     for row in betting_page.find_all('div', {'class': 'eventLine-value'}):
#         teams_list.append(row.text)
#     betting_lines = []
#     for item in betting_page.find_all('div', {'class': 'event-holder holder-complete'}):
#         for line in item.find('div', {'class': 'el-div eventLine-book'}):
#             betting_lines.append(line.text)
#     betting_lines = [line.replace('\xa0', ' ') for line in betting_lines]
#     date_list = [date for item in betting_lines]
#     zipped_teams_lines = zip(date_list, teams_list, betting_lines)
#     return list(zipped_teams_lines)
#
#
# # Get betting line moneylines
# def get_betting_mls(date):
#     info_list = []
#     betting_page = requests.get(
#         f'https://classic.sportsbookreview.com/betting-odds/nba-basketball/money-line/?date={date}')
#     time.sleep(2)
#     betting_page = BeautifulSoup(betting_page.text, 'html.parser')
#     teams_list = []
#     for row in betting_page.find_all('div', {'class': 'eventLine-value'}):
#         teams_list.append(row.text)
#     betting_lines = []
#     for item in betting_page.find_all('div', {'class': 'event-holder holder-complete'}):
#         for line in item.find('div', {'class': 'el-div eventLine-book'}):
#             betting_lines.append(line.text)
#     betting_lines = [line.replace('\xa0', ' ') for line in betting_lines]
#     date_list = [date for item in betting_lines]
#     zipped_teams_lines = zip(date_list, teams_list, betting_lines)
#     return list(zipped_teams_lines)
#
# date_list = {'20210108', '20210117', '20210211', '20210209', '20210118', '20210225', '20210128', '20210114', '20201223', '20210201', '20210102', '20210303', '20210123', '20210130', '20201228', '20210104', '20210217', '20210203', '20201231', '20210215', '20210111', '20210121', '20210106', '20210210', '20210221', '20210228', '20210116', '20210304', '20210126', '20210205', '20210224', '20210220', '20210227', '20210124', '20210120', '20201226', '20210218', '20210216', '20210301', '20210204', '20210125', '20201222', '20210101', '20210119', '20210112', '20210226', '20210202', '20210302', '20210129', '20210110', '20210207', '20210127', '20210212', '20210107', '20210214', '20210122', '20201230', '20210219', '20210223', '20201229', '20210113', '20210206', '20210222', '20210105', '20210131', '20210213', '20201227', '20210115', '20210109', '20210103', '20201225', '20210208'}
#
# all_spreads = []
# all_money_lines = []
# all_totals = []
# for date in date_list:
#     all_spreads.append(get_betting_spreads(date))
#     all_money_lines.append(get_betting_mls(date))
#     all_totals.append(get_betting_totals(date))
#
# print(len(all_spreads), len(all_money_lines), print(len(all_totals)))
# print("----------")
# print(all_money_lines)
# print("----------")
# print(all_spreads)
# print("----------")
# print(all_totals)

# Get current day games and lines

#
# #get current date in number format
# cur_date = str(date.today()).replace('-', '')
# betting_page = requests.get(f'https://classic.sportsbookreview.com/betting-odds/')
#
#
# betting_page = BeautifulSoup(betting_page.text, 'html.parser')
# teams_list = []
# print(betting_page)
# for row in betting_page.find_all('div', {'class': 'eventLine-value'}):
#     teams_list.append(row.text)
#     print(row)
# betting_lines = []
# for item in betting_page.find_all('div', {'class': 'event-holder holder-complete'}):
#     for line in item.find_all('div', {'class': 'el-div eventLine-book'}):
#         if line.text != '':
#             betting_lines.append(line.text)
#             break
#
# betting_lines = [line.replace('\xa0', ' ') for line in betting_lines]