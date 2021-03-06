%%timeit
## This file consumes retrosheet data - information about the source file can be found here:
##https://www.retrosheet.org/eventfile.htm
import pandas as pd
import numpy as np
import glob
import os
from timeit import default_timer as timer

#Set Start Time
start = timer()

#Import data set from folder
#os.chdir("/home/aaronhaag/EW/EffectivelyWild/Games")
#extension = "*"
#all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#df = pd.concat([pd.read_csv(f,header = None, names=['Type','Info1', 'Info2', 'Info3', 'Info4', 'Info5', 'Info6', 'Info7']) for f in all_filenames])

#Set up global variables
game_id_list = []
active_pitcher_list = []
hap = None
aap = None
number_of_homers = []
number_of_pitchers = []

#Import Data Set from CSV
df = pd.read_csv('Games/2016CHN.EVN', header = None, names=['Type','Info1', 'Info2', 'Info3', 'Info4', 'Info5', 'Info6', 'Info7'])

#Set the Home Pitcher
def home_pitcher(row, hap):
    if (row.Type == "start" and row.Info3 == "1" and row.Info5 == "1"):
        return row.Info1
    if (row.Type == "sub" and row.Info3 == "1" and row.Info5 == "1"):
        return row.Info1
    return hap

#Set the Away Pitcher
def away_pitcher(row, aap):
    if (row.Type == "start" and row.Info3 == "0" and row.Info5 == "1"):
        return row.Info1
    if (row.Type == "sub" and row.Info3 == "0" and row.Info5 == "1"):
        return row.Info1
    return aap

#Generate a list that has the Active Pitcher Id for Plays and None for Non-Plays
def set_active_pitcher(row, hap, aap):
    if row.Type == "play" and row.Info2 == "0":
        return hap
    if row.Type == "play" and row.Info2 == "1":
        return aap

#Return the number of Homeruns for a player from teh homeruns dataframe
def count_home_runs(row, hrs):
    return sum(x == row.player_id for x in hrs['Info3'])

#Return the number of Unique Pitchers for Each Home Run Hitter
def count_pitchers(row, hrs):
    hitter = hrs.loc[hrs['Info3'] == row.player_id]
    pitchers = hitter.Pitcher.unique()
    return len(pitchers)


#Assign Game Id and Pitcher Id to Rows
for line, row in enumerate(df.itertuples(), 1):
    if row.Type == "id":
        gameId = row.Info1
    game_id_list.append(gameId)
    hap = home_pitcher(row,hap)
    aap = away_pitcher(row, aap)
    active_pitcher_list.append(set_active_pitcher(row, hap, aap))
df.insert(0, "GameId", game_id_list, True)
df.insert(1, "Pitcher", active_pitcher_list, True)

#Create dataframes for Games and Plays
games = df.loc[df["Type"] == "id", "GameId"]
plays = df.loc[df["Type"] == "play", ["GameId", "Pitcher", "Info1", "Info2", "Info3", "Info4", "Info5", "Info6"]]

#Create a dataframe for only Home Runs
plays = plays.replace('NAN', np.nan)
is_HR = plays['Info6'].str.contains(r'HR', na=True)
homeruns = plays[is_HR]


#Create a dataframe containing one row for all players who have homered
hr_hitters_list = homeruns.Info3.unique()
hr_hitters = pd.DataFrame(hr_hitters_list)
hr_hitters.columns = ['player_id']

#Count the number of Homeruns for each player and pitchers for each player
for line, row in enumerate(hr_hitters.itertuples(), 1):
    number_of_homers.append(count_home_runs(row, homeruns))
    number_of_pitchers.append(count_pitchers(row, homeruns))
hr_hitters.insert(1, "Homeruns", number_of_homers, True)
hr_hitters.insert(2, "Pitchers", number_of_pitchers, True)

print(hr_hitters.head())
end = timer()
print((end-start)*1000)

#Export data frame to csv for testing
#hr_hitters.to_csv(r'/home/aaronhaag/EW/homerunratio3.csv', header=True)
