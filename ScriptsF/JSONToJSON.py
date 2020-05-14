import os
import numpy as np
import pandas as pd
import json
import re

BaseDir = "/run/media/dopeboy/Data/Documents/News Aggregator/DataSet"
SubDirList = os.listdir(BaseDir)
Allowed = []
for SubDir in SubDirList:
    if(SubDir not in Allowed):
        continue
    WorkPath = os.path.join(BaseDir, SubDir)
    FileList = os.listdir(WorkPath)
    DirCap = len(FileList)
    ChooseList = np.random.randint(low=0, high=DirCap, size=25000, dtype="int")
    ChooseList = list(set(ChooseList))
    Limit = len(ChooseList)
    if (Limit > 15000):
        Limit = 15000 - 737
    ChooseList = ChooseList[:Limit]
    IntSportsPath = os.path.join(BaseDir, "JSONSports")
    IntSportsList = os.listdir(IntSportsPath)
    DStore = pd.DataFrame()
    for FileName in IntSportsList:
        FilePath = os.path.join(IntSportsPath, FileName)
        print(FilePath)
        JData = json.load(open(file=FilePath, mode="r",
                               encoding="utf-8", errors="ignore"))
        Row = pd.DataFrame([JData])
        Row = Row["text"]
        Row[0] = re.sub('[^a-zA-Z ]+', ' ', Row[0])
        if(len(Row) > 0):
            DStore = DStore.append(Row, ignore_index=True)
    for FileNum in ChooseList:
        FilePath = os.path.join(WorkPath, FileList[FileNum])
        print(FilePath)
        JData = json.load(open(file=FilePath, mode="r",
                               encoding="utf-8", errors="ignore"))
        Row = pd.DataFrame([JData])
        Row = Row["text"]
        Row[0] = re.sub('[^a-zA-Z ]+', ' ', Row[0])
        if(len(Row) > 0):
            DStore = DStore.append(Row, ignore_index=True)
    # print(SubDir)
    DStore = DStore.rename(columns={0: "text"})
    # print(DStore.head())
    JSONPath = "/run/media/dopeboy/Data/Documents/News Aggregator/" + SubDir + ".json"
    DStore.to_json(JSONPath)
