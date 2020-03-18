# Classifier functions

import pickle

import nltk
import pandas as pd
from nltk.corpus import stopwords

# from nltk.tokenize import punkt
# from nltk.corpus.reader import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

import classifier_help as clh

path_models = "Models/"

# KNN
path_knn = path_models + "best_knnc_2.pickle"
with open(path_knn, "rb") as data:
    knn_model = pickle.load(data)

path_tfidf = "pickles/tfidf.pickle"
with open(path_tfidf, "rb") as data:
    tfidf = pickle.load(data)

# Category mapping dictionary
category_codes = {"first": 1, "second": 2, "third": 3}

category_names = {1: "first", 2: "second", 3: "third"}

# Needs to be altered to be consistent with the feature engineering that I developed earlier

punctuation_signs = list('?:!.,;"()')
stop_words = list(stopwords.words("english"))
pronouns = [
    "i",
    "im",
    "ive",
    "id",
    "my",
    "me",
    "myself",
    "we",
    "wed",
    "weve",
    "us",
    "our",
    "ours",
    "ourselves",
    "you",
    "youre",
    "youve",
    "youd",
    "your",
    "yourself",
    "yourselves",
    "he",
    "hes",
    "hed",
    "hell",
    "him",
    "his",
    "himself",
    "she",
    "shes",
    "shell",
    "shed",
    "her",
    "hers",
    "herself",
    "they",
    "them",
    "their",
    "theirs",
    "themself",
    "themselves",
]
stop_words_wo_pronouns = [word for word in stop_words if word not in pronouns]


def clean_text_df(df, col="text"):
    lemmatized_text_list = []

    df["text_Parsed_1"] = df[col].str.replace("\r", " ")
    df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("\n", " ")
    df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("    ", " ")
    df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("'s'", "")
    df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("'", "")
    df["text_Parsed_2"] = clh.no_punctuation(df["text_Parsed_1"], quotes=True)
    df["text_Parsed_3"] = df["text_Parsed_2"]
    # df["text_Parsed_3"] = [clh.replace_quotes(text) for text in df["text_Parsed_2"]]
    for punct_sign in punctuation_signs:
        df["text_Parsed_3"] = df["text_Parsed_3"].str.replace(punct_sign, "")
    for punct_sign_sp in list("-/"):
        df["text_Parsed_3"] = df["text_Parsed_3"].replace(punct_sign_sp, " ")
    df["text_Parsed_4"] = df["text_Parsed_3"].str.replace("'s", "")
    wordnet_lemmatizer = WordNetLemmatizer()
    print("processed1")
    for i in range(len(df)):
        lemmatized_list = []
        text = df.iloc[i]["text_Parsed_4"]
        text_words = text.split(" ")
        for word in text_words:
            lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
        lemmatized_text = " ".join(lemmatized_list)
        lemmatized_text_list.append(lemmatized_text)
    df["text_Parsed_5"] = lemmatized_text_list
    print("lemmatized")
    df["text_Parsed_6"] = df["text_Parsed_5"]
    for stop_word in stop_words_wo_pronouns:
        regex_stopword = r"\b" + stop_word + r"\b"
        df["text_Parsed_6"] = df["text_Parsed_6"].str.replace(regex_stopword, "")
    df = df.drop(
        [
            "text_Parsed_1",
            "text_Parsed_2",
            "text_Parsed_3",
            "text_Parsed_4",
            "text_Parsed_5",
        ],
        axis=1,
    )
    df = df.rename(columns={"text_Parsed_6": col+"_Parsed"})
    # print(df.head())

    # TF-IDF
    # features = tfidf.transform(df).toarray()

    return df


def designate_person_from_df(df):

    # Dataframe creation
    # df = pd.DataFrame(columns=["text"])
    # df.loc[0] = text

    # print(df.head())

    pred_list = []
    # TF-IDF
    for i in range(len(df)):
        texts = df["text_Parsed"]
        features = tfidf.transform([texts[i]]).toarray()

        prediction_knn = knn_model.predict(features)[0]
        # prediction_knn_proba = knn_model.predict_proba(create_features_from_text(text))[0]

        # Return result
        category_knn = get_category_name(prediction_knn)

        pred_list.append(category_knn)
    return pred_list

    # return features


# def create_features_from_text(text):

#     # Dataframe creation
#     lemmatized_text_list = []
#     df = pd.DataFrame(columns=["text"])
#     df.loc[0] = text
#     df["text_Parsed_1"] = df["text"].str.replace("\r", " ")
#     df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("\n", " ")
#     df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("    ", " ")
#     df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("'s'", "")
#     df["text_Parsed_1"] = df["text_Parsed_1"].str.replace("'", "")
#     df["text_Parsed_2"] = clh.no_punctuation(df["text_Parsed_1"], quotes=True)
#     df["text_Parsed_3"] = [
#         clh.replace_quotes(text) for text in df["text_Parsed_2"]
#     ]
#     for punct_sign in punctuation_signs:
#         df["text_Parsed_3"] = df["text_Parsed_3"].str.replace(punct_sign, "")
#     for punct_sign_sp in list("-/"):
#         df["text_Parsed_3"] = df["text_Parsed_3"].replace(punct_sign_sp, " ")
#     df["text_Parsed_4"] = df["text_Parsed_3"].str.replace("'s", "")
#     wordnet_lemmatizer = WordNetLemmatizer()
#     lemmatized_list = []
#     text = df.loc[0]["text_Parsed_4"]
#     text_words = text.split(" ")
#     for word in text_words:
#         lemmatized_list.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
#     lemmatized_text = " ".join(lemmatized_list)
#     lemmatized_text_list.append(lemmatized_text)
#     df["text_Parsed_5"] = lemmatized_text_list
#     df["text_Parsed_6"] = df["text_Parsed_5"]
#     for stop_word in stop_words_wo_pronouns:
#         regex_stopword = r"\b" + stop_word + r"\b"
#         df["text_Parsed_6"] = df["text_Parsed_6"].str.replace(regex_stopword, "")
#     df = df["text_Parsed_6"]
#     df = df.rename(columns={"text_Parsed_6": "text_Parsed"})
#     # print(df.head())

#     # TF-IDF
#     features = tfidf.transform(df).toarray()

#     return features


def get_category_name(category_id):
    for category, id_ in category_codes.items():
        if id_ == category_id:
            return category


# def predict_from_text(text):

#     # Predict using the input model
#     prediction_knn = knn_model.predict(create_features_from_text(text))[0]
#     # prediction_knn_proba = knn_model.predict_proba(create_features_from_text(text))[0]

#     # Return result
#     category_knn = get_category_name(prediction_knn)
#     return category_knn

#     # print("The predicted category using the KNN model is %s." %(category_knn) )
#     # print("The conditional probability is: %a" %(prediction_knn_proba.max()*100))


# def predict_from_text_list(in_list):
#     pred_list = []
#     for text in in_list:
#         prediction = predict_from_text(text)
#         pred_list.append(prediction)
#     return pred_list


# predict_from_text("I am a cat, I am I am I am.")
