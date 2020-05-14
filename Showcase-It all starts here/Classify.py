import os
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import re
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle
import joblib
import spacy


TypeDict = {
    0: "Entertainment",
    1: "Financial",
    2: "Politics",
    3: "Sports",
    4: "Technology",
    5: "Others"
}

ClassifyDict = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: []
}

Lemmatizer = WordNetLemmatizer()

BasePath = os.path.dirname(os.path.realpath(__file__))
DataSetPath = os.path.join(BasePath, r"ScrapedData")
JSONList = os.listdir(DataSetPath)
OutPath = os.path.join(BasePath, "CleanText")
nlp = spacy.load("en_vectors_web_lg")

def GetClusters(GenreList):
    if(len(GenreList) == 0):
        return []
    ClusterList = []
    for i in GenreList:
        CleanFileName = os.path.join(OutPath, str(i) + ".txt")
        data = open(CleanFileName,'r').read()
        ClusterList.append(nlp(data))

    flag = 0
    add_cluster = 0
    result_clusters = []
    visited = set()

    for j in range(len(ClusterList)):
        add_cluster = 0
        if(flag == 0):
            num = set()
            num.add(j)
            visited.add(j)
            result_clusters.append(num)
            flag = 1
        else:
            for cluster_num in range(len(result_clusters)):
                if(j in visited):
                    break
                cluster_set = result_clusters[cluster_num]
                mean = 0
                for val in cluster_set:
                    mean += (ClusterList[j].similarity(ClusterList[val]))
                mean /= len(cluster_set)
                if(mean > 0.927):
                    cluster_set.add(j)
                    visited.add(j)
                    add_cluster = 1
            if(add_cluster == 0):
                num = set()
                num.add(j)
                visited.add(j)
                result_clusters.append(num)

    result_list = []


    for cluster_set in result_clusters:
        new_cluster = set()
        for elem in cluster_set:
            new_cluster.add(GenreList[elem])
        result_list.append(new_cluster)
    
    return result_list



def NLTK2WNTag(NLTKTag):
    if NLTKTag.startswith("J"):
        return wordnet.ADJ
    elif NLTKTag.startswith("V"):
        return wordnet.VERB
    elif NLTKTag.startswith("N"):
        return wordnet.NOUN
    elif NLTKTag.startswith("R"):
        return wordnet.ADV
    else:
        return None


def LemmatizeSent(Sentence):
    NLTKTagged = nltk.pos_tag(nltk.word_tokenize(Sentence))
    WNTagged = map(lambda x: (x[0], NLTK2WNTag(x[1])), NLTKTagged)
    ResultWords = []
    for Word, Tag in WNTagged:
        if Tag is None:
            ResultWords.append(Word)
        else:
            ResultWords.append(Lemmatizer.lemmatize(Word, Tag))
    return " ".join(ResultWords)



def GenerateFinJSON(ClusterDict):
    FinalFile = {}
    for key in ClusterDict:
        DictList = []
        for ClusterList in ClusterDict[key]:
            TempList = []
            for i in ClusterList:
                FilePath = os.path.join(DataSetPath,str(i) +".json")
                with open(file=FilePath, mode='r', errors="ignore") as TextFile:
                    JSONData = TextFile.read()
                Articles = json.loads(JSONData)
                TempList.append(Articles)
            DictList.append(TempList)
        FinalFile[key] = DictList
    return FinalFile



def main():
    print("Modules loaded")
    
    StopWords = set(stopwords.words("english"))
    ClassifyPath = os.path.join(BasePath, "SVMModels")
    FeaturePath = os.path.join(ClassifyPath, "FeatureNames.csv")
    ColumnNames = list( pd.read_csv(FeaturePath)["FeatureName"] )    
    ColumnNames.remove("CATEGORY")
    ColumnLen = len(ColumnNames)
    print("Features loaded")

    for JSON in JSONList:
        FilePath = os.path.join(DataSetPath, JSON)
        JSONData = ""
        with open(file=FilePath, mode='r', errors="ignore") as TextFile:
            JSONData = TextFile.read()
        Articles = json.loads(JSONData)
        Articles = Articles["Text"]

        Articles = re.sub("[^a-zA-Z ]+", " ", Articles)
        Articles = Articles.lower()
        Articles = Articles.split()
        Articles = [word for word in Articles if not word in StopWords]
        Articles = [word for word in Articles if not word in ENGLISH_STOP_WORDS]
        Articles = " ".join(Articles)
        Articles = LemmatizeSent(Articles)
        Name = int(JSON[:-5])

        OccurFrame = []
        for i in range(ColumnLen):
            OccurFrame.append(0)
        for i in range(ColumnLen):
            if(ColumnNames[i] in Articles):
                OccurFrame[i] = 1
        OccurFrame = np.asarray(OccurFrame,dtype=int)
        OccurFrame = OccurFrame.reshape(1,-1)
        PredictList = []
        for i in range(5):
            ModelName = "SVM" + str(i) + ".pkl"
            ModelPath = os.path.join(ClassifyPath, ModelName)
            Classifier = joblib.load(ModelPath)
        
            PredictedProb = (list(Classifier.predict_proba(OccurFrame)[0]))
            print(Name)
            print(PredictedProb)
            PredictList.append(PredictedProb[1])
            
        OtherThres = 0.2

        if(max(PredictList) > OtherThres):
            Classification = PredictList.index(max(PredictList))
            ClassifyDict[Classification].append(Name)

        else:
            ClassifyDict[5].append(Name)


        OutFile = os.path.join(OutPath, JSON[:-5] + ".txt")
        NewFile = open(OutFile, "w")
        NewFile.write(Articles)

    ClusterDict = {}
    for Key in ClassifyDict.keys():
        ClusterDict[TypeDict[Key]] = GetClusters(ClassifyDict[Key])
    print(ClusterDict)
    
    FinalFile = GenerateFinJSON(ClusterDict)
    with open('DataSet.jsonp', 'w') as FilePoint:
        json.dump(FinalFile, FilePoint)

    with open(file="DataSet.jsonp", mode="r", encoding="utf-8", errors="ignore") as TextFile:
        JSONData = TextFile.read()

    JSONData = r"MyData = [" + JSONData + r"]"

    with open(file="DataSet.jsonp", mode="w", encoding="utf-8") as TextFile:
        TextFile.write(JSONData)

    

if __name__ == "__main__":
    main()