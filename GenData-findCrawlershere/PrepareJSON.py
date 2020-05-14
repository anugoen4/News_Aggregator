import os
import json
import re
import pandas as pd


# for RowNum in range(JData.shape[0]):

def main():

    with open(file="Output.json", mode="r", encoding="utf-8", errors="ignore") as TextFile:
        JSONData = TextFile.read()
    JSONData = re.sub('\]\[', ',', JSONData)
    with open(file="Output.json", mode="w", encoding="utf-8") as TextFile:
        TextFile.write(JSONData)

    JData = json.load( open(file="Output.json", mode="r", encoding="utf-8", errors="ignore") )
    JData = pd.DataFrame(JData)

    for RowNum in range(JData.shape[0]):
        RowFrame = JData.iloc[RowNum]
        if(RowFrame["Text"] != "" and RowFrame["ImgLink"] != ""):
            FileName = os.path.join("ScrapedData", str(RowNum) + ".json")
            RowFrame.to_json(FileName)
            with open(file=FileName, mode="r", encoding="utf-8", errors="ignore") as TextFile:
                JSONData = TextFile.read()
            JSONData = re.sub('\\\/', '/', JSONData)
            with open(file=FileName, mode="w", encoding="utf-8") as TextFile:
                TextFile.write(JSONData)

if __name__ == "__main__":
    main()