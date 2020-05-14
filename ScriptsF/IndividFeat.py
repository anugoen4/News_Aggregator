import re
import os
import json
import pandas as pd
import numpy as np

FinFeat = pd.read_csv("FinalFeaturesFin.csv")
GenreSeries = FinFeat.iloc[:,-1]
FinFeat = FinFeat.drop(columns="CATEGORY")

for i in range(5):
    TempSeries = GenreSeries.copy()
    for j in range(len(TempSeries)):
        if(TempSeries[j] == i):
            TempSeries[j] = 1
        else:
            TempSeries[j] = 0
    TempFeat = FinFeat.copy()
    TempFeat["CATEGORY"] = TempSeries
    OutName = "TempFeat" + str(i) + ".csv"
    TempFeat.to_csv(OutName, index = False)