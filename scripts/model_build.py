import pandas as pd
import pickle as pickle
from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np

import import_func as imp
import classifier_help as clh
import classifier_func as cls

path_df = "pickles/hand_coded_ALL.pickle"
# full_filename = "../data/by_article_fulltext_112919-2.jl" # OLD VERSION
full_filename = "../data/by_article_fulltext_020920.jl"


with open(path_df, 'rb') as data:
    coded_df = pickle.load(data)

df_full = imp.init_df(full_filename, "full", "df")

# print(len(coded_df))

df = coded_df.merge(right=df_full, how="left", left_on="id", right_index=True)

# df["Content"] = df["text"]

df = cls.clean_text_df(df)


# print(df.loc[280]['input'])
# print(df.loc[280]['text_Parsed'])
df = df.rename(columns={"input": "Category_Code"})
df = clh.category(df)


X_train, X_test, y_train, y_test = train_test_split(df['text_Parsed'], 
                                                    df['Category_Code'], 
                                                    test_size=0.15, 
                                                    random_state=8)

# print(X_train.head())
# print(X_test.head())
# print(y_train.head())
# print(y_test.head())

# Parameter election
ngram_range = (1,2)
min_df = 10
max_df = 1.
max_features = 300


tfidf = TfidfVectorizer(encoding='utf-8',
                        ngram_range=ngram_range,
                        stop_words=None,
                        lowercase=False,
                        max_df=max_df,
                        min_df=min_df,
                        max_features=max_features,
                        norm='l2',
                        sublinear_tf=True)
                        
features_train = tfidf.fit_transform(X_train).toarray()
labels_train = y_train
print(features_train.shape)

features_test = tfidf.transform(X_test).toarray()
labels_test = y_test
print(features_test.shape)


category_codes = {
    1:'first',
    2:'second',
    3:'third'
}


for Product, category_id in sorted(category_codes.items()):
    features_chi2 = chi2(features_train, labels_train == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    # print("# '{}' category:".format(Product))
    # print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-5:])))
    # print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-2:])))
    # print("")



