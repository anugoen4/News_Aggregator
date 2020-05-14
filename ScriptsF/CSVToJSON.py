import os
import re
import pandas as pd

BaseDir = "/run/media/dopeboy/Data/Documents/News Aggregator/DataSet"
CSVPath = os.path.join(BaseDir, "Politics.csv")
CSVData = pd.read_csv(CSVPath)
CSVData = pd.DataFrame(CSVData["Content"])
CSVData = CSVData.rename(columns={"Content": "Text"})
CSVData.to_json(
    "/run/media/dopeboy/Data/Documents/News Aggregator/DataSet/Politics.json")
