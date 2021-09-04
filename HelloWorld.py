import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pybaseball import batting_stats

b_2019 = batting_stats(2019,2019)

indexNames = b_2019[b_2019['PA']<502].index
b_2019.drop(indexNames, inplace = True)

b_2019.head()

#msg = "Hello World!"
#print(msg)

#ewSite = pd.read_html('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2020&month=0&season1=2019&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=', match='Mike Trout')
#print(ewSite[0].head)

#ly = ewSite[0]