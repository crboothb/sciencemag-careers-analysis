# Start KNN notebook

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from pprint import pprint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Dataframe
path_df = "pickles/df.pickle"
with open(path_df, "rb") as data:
    df = pickle.load(data)

# features_train
path_features_train = "pickles/features_train.pickle"
with open(path_features_train, "rb") as data:
    features_train = pickle.load(data)

# labels_train
path_labels_train = "pickles/labels_train.pickle"
with open(path_labels_train, "rb") as data:
    labels_train = pickle.load(data)

# features_test
path_features_test = "pickles/features_test.pickle"
with open(path_features_test, "rb") as data:
    features_test = pickle.load(data)

# labels_test
path_labels_test = "pickles/labels_test.pickle"
with open(path_labels_test, "rb") as data:
    labels_test = pickle.load(data)


print(features_train.shape)
print(features_test.shape)


knnc_0 = KNeighborsClassifier()

# Create the parameter grid
n_neighbors = [int(x) for x in np.linspace(start=1, stop=100, num=100)]

param_grid = {"n_neighbors": n_neighbors}

# Create a base model
knnc = KNeighborsClassifier()

# Manually create the splits in CV in order to be able to fix a random_state (GridSearchCV doesn't have that argument)
cv_sets = ShuffleSplit(n_splits=3, test_size=0.33, random_state=8)

# Instantiate the grid search model
grid_search = GridSearchCV(
    estimator=knnc, param_grid=param_grid, scoring="accuracy", cv=cv_sets, verbose=1
)

# Fit the grid search to the data
grid_search.fit(features_train, labels_train)


n_neighbors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
param_grid = {"n_neighbors": n_neighbors}

knnc = KNeighborsClassifier()
cv_sets = ShuffleSplit(n_splits=3, test_size=0.33, random_state=8)

grid_search = GridSearchCV(
    estimator=knnc, param_grid=param_grid, scoring="accuracy", cv=cv_sets, verbose=1
)

grid_search.fit(features_train, labels_train)

best_knnc = grid_search.best_estimator_

best_knnc.fit(features_train, labels_train)
knnc_pred = best_knnc.predict(features_test)

# Training accuracy
print("The training accuracy is: ")
print(accuracy_score(labels_train, best_knnc.predict(features_train)))
print("the test accuracy is: ")
print(accuracy_score(labels_test, knnc_pred))

aux_df = (
    df[["Category", "Category_Code"]].drop_duplicates().sort_values("Category_Code")
)
conf_matrix = confusion_matrix(labels_test, knnc_pred)
plt.figure(figsize=(12.8, 6))
sns.heatmap(
    conf_matrix,
    annot=True,
    xticklabels=aux_df["Category"].values,
    yticklabels=aux_df["Category"].values,
    cmap="Blues",
)
plt.ylabel("Predicted")
plt.xlabel("Actual")
plt.title("Confusion matrix")
plt.show()

d = {
    "Model": "KNN",
    "Training Set Accuracy": accuracy_score(
        labels_train, best_knnc.predict(features_train)
    ),
    "Test Set Accuracy": accuracy_score(labels_test, knnc_pred),
}

df_models_knnc = pd.DataFrame(d, index=[0])

print(df_models_knnc)

with open("Models/best_knnc_2.pickle", "wb") as output:
    pickle.dump(best_knnc, output)

with open("Models/df_models_knnc_2.pickle", "wb") as output:
    pickle.dump(df_models_knnc, output)
