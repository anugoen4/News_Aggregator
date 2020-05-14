import re
import os
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectKBest

BasePath = os.path.dirname( os.path.realpath(__file__) )
#Assuming the dataset is in the same folder
DataPath = os.path.join(BasePath, "CleanDataSet")

print("Start")

DataTypeList = os.listdir(DataPath)
FileList = []
Labels = []
TypeDict = {
    "Entertainment": 0,
    "Financial": 1,
    "Politics": 2,
    "Sports": 3,
    "Technology": 4
}

for Type in DataTypeList:
    InputPath = os.path.join(DataPath, Type)
    TempFileList = os.listdir(InputPath)
    i = 0
    #while( i < len(TempFileList) ):
    while( i < 4000 ):
        Labels.append(TypeDict[Type])
        TempFile = os.path.join(InputPath, TempFileList[i])
        FileList.append(TempFile)
        i += 1

print("FileList Prepared")

Vectorizer = TfidfVectorizer(input = 'filename', min_df = 50, norm = "l2", sublinear_tf=True, ngram_range=(1, 2))

Vectors = Vectorizer.fit_transform(FileList)
FeatureNames = Vectorizer.get_feature_names()
DenseList = Vectors.todense().tolist()

print("Calculation Done")

VectorFrame = pd.DataFrame(DenseList, columns=FeatureNames)

KBest = SelectKBest(score_func=chi2, k="all")
KBestFeatures = KBest.fit(Vectors, Labels)

print("Features Chosen")

ScoreFrame = pd.DataFrame(KBestFeatures.scores_)
ColumnFrame = pd.DataFrame(FeatureNames)

FeatureScores = pd.concat([ColumnFrame, ScoreFrame], axis=1)
FeatureScores.columns = ["Specs", "Score"]
print(type(FeatureScores))
FeatureScores = FeatureScores.nlargest(2300, "Score")
SpecsSet = set(FeatureScores["Specs"])
ColumnSet = set(FeatureNames)
SpecsSet = ColumnSet - SpecsSet

print("Features Selected")

VectorFrame = VectorFrame.drop(columns=list(SpecsSet))

print("Features Dropped")

VectorFrame["CATEGORY"] = Labels

VectorFrame.to_csv("FinalFeaturesFin2.csv", index=False)

print("Saved")