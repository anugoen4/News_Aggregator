import os
import numpy as np
import pandas as pd
import json
import re

BaseDir = "F:\Downloads\GenData\ScrapedData"
SubDirList = os.listdir(BaseDir)

for SubDir in SubDirList:
    WorkPath = os.path.join(BaseDir, SubDir)
    FileList = os.listdir(WorkPath)
    DStore = pd.DataFrame()
    for FileName in FileList:
        FilePath = os.path.join(WorkPath, FileName)
        print(FilePath)
        JData = json.load(open(file=FilePath, mode="r",
                               encoding="utf-8", errors="ignore"))
        Row = pd.DataFrame([JData])
        Row = Row["Text"]
        Row[0] = re.sub('[^a-zA-Z ]+', ' ', Row[0])
        if(len(Row) > 0):
            DStore = DStore.append(Row, ignore_index=True)
    DStore = DStore.rename(columns={0: "Text"})
    OutFileName = SubDir + ".json"
    JSONPath = os.path.join("F:\Downloads\GenData\ScrapedData", OutFileName)
    DStore.to_json(JSONPath)
