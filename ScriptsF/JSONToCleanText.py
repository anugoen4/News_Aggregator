# Importing the Libraries
import os
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from pandas import ExcelWriter
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

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")

# Functions Defined


def nltk2wn_tag(nltk_tag):
    if nltk_tag.startswith("J"):
        return wordnet.ADJ
    elif nltk_tag.startswith("V"):
        return wordnet.VERB
    elif nltk_tag.startswith("N"):
        return wordnet.NOUN
    elif nltk_tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)
    res_words = []
    for word, tag in wn_tagged:
        if tag is None:
            res_words.append(word)
        else:
            res_words.append(lemmatizer.lemmatize(word, tag))
    return " ".join(res_words)


# Initializer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Code
BasePath = os.path.dirname(os.path.realpath(__file__))
DataSetPath = os.path.join(BasePath, r"DataSetJSONs")
JSONList = os.listdir(DataSetPath)

print("Start")
for JSON in JSONList:
    print(JSON)
    FilePath = os.path.join(DataSetPath, JSON)
    Articles = pd.DataFrame(
        json.load(
            open(file=FilePath, mode="r", encoding="utf-8", errors="ignore")
        )
    )
    if("Entertainment" in JSON or "Financial" in JSON):
        Articles = Articles["text"].tolist()
    else:
        Articles = Articles["Text"].tolist()
    print(len(Articles))
    i = 0
    OutPath = os.path.join(BasePath, "CleanDataSet")
    processed_articles = []
    for Article in Articles:
        Article = re.sub("[^a-zA-Z ]+", " ", Article)
        Article = Article.lower()
        Article = Article.split()
        Article = [word for word in Article if not word in stop_words]
        Article = [word for word in Article if not word in ENGLISH_STOP_WORDS]
        Article = " ".join(Article)
        Article = lemmatize_sentence(Article)
        OutFile = os.path.join(OutPath, JSON[:-5], str(i) + ".txt")
        NewFile = open(OutFile, "w")
        NewFile.write(Article)
        i += 1