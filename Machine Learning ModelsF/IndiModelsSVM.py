# Classification template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Importing the dataset


for i in range(5):
    ReadModelName = "TempFeat" + str(i) + ".csv"
    dataset = pd.read_csv(ReadModelName)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    print("Start")

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 10)

    from sklearn.preprocessing import Binarizer
    sc_X = Binarizer(0)
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.fit_transform(X_test)

    from sklearn.linear_model import LogisticRegression
    classifier = SVC(C = 10, degree = 3,gamma = 0.01, kernel = 'rbf', decision_function_shape= 'ovr',probability=True)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)

    print(cm)

    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_test,y_pred))


    from sklearn.externals import joblib
    OutModelName = "SVM" + str(i) + ".pkl"  
    joblib.dump(classifier, OutModelName)
