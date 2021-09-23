import pandas as pd
import numpy as np
import glob
import os
from timeit import default_timer as timer


data = [["Bryant", "Scherzer"], ["Bryant", "Scherzer"],["Bryant", "Haag"], ["Bryant", "Strasburg"], ["Rizzo", "Scherzer"]]
df = pd.DataFrame(data, columns = ["hitter", "pitcher"])
df.set_index("hitter")

pitchers = df.groupby("hitter").nunique("pitcher").reset_index("hitter")
hrCount = df.groupby("hitter").size().to_frame(name="hrs").reset_index("hitter")
pitchers.insert(1, "hrs", hrCount['hrs'], True)

print(df)
print(pitchers)
print(hrCount)