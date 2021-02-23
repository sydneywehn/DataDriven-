import pandas as pd


# Process raw data from sportsbook review
df = pd.read_csv('nba odds 2020-21.csv')
#print(df.head())

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

print(final_df.head())
