%%timeit
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

#Create a dataframe for only Home Runs
df = df.replace("NAN", np.nan)
is_HR = (df["Info6"].str.contains(r'HR', na=True)) & (df["Type"] == "play")
hrs = df[is_HR]
homeruns = hrs[["Info3", "Pitcher"]].copy()

#Count the number of Homeruns and pitchers wihtout iterating
pitchers = homeruns.groupby("Info3").nunique("Pitcher").reset_index("Info3")
hrCount = homeruns.groupby("Info3").size().to_frame(name="hrs").reset_index("Info3")
pitchers.insert(1, "hrs", hrCount['hrs'], True)
pitchers.rename(columns={"Info3": "PlayerId", "hrs":"Hrs", "Pitcher" : "Pitchers"}, inplace=True)


print(pitchers.head())
end = timer()
print((end-start)*1000)

#Export data frame to csv for testing
#pitchers.to_csv(r'/home/aaronhaag/EW/homerunratio2.csv', header=True)
