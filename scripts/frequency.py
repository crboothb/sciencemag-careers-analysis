import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
stops = stopwords.words('english')
stops_dict = {}
for word in stops:
    stops_dict[word]=""

import classifier_help as clh



def freq_workflow(df, n_facets, extras, lemm=False):
    stops = stopwords.words('english')
    interval = int(24/n_facets)
    stops_dict = {}
    facets = {}

    for word in stops:
        stops_dict[word]=""

    for i in range(n_facets):
        start = i*interval+1996
        end = start+interval
        facets[start] = df[(df.year<=start) & (df.year <end)]
    
    for keya in facets:

        text_list = facets[keya]["text"]

        word_dict = word_frequency(text_list, stops_dict, extra_stops=extras, lemm=lemm)

        top = dict_to_top(word_dict, 40)
        # print(top)
        # print(top["word"])
        plt.figure(figsize=(12, 10))
        plt.barh(top["word"],top["freq"])
        # plt.savefig(str(keya)+"-frequency.png")

def add_to_freq_dict(text, word_dict): #, lemm=False
    text = " ".join(text.split())
    for word in text.split(" "):
        # if lemm==True:
        #     word = lemmatize_word(word)
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return(word_dict)

def lemmatize_text(text):
    weird_plurals = {"postdocs":"postdoc","students":"student","scientists":"scientist","says":"say"}
    text = " ".join(text.split())
    lemm_text=[]
    for word in text.split(" "):
        # if word == "says":
        #     print(word)
        #     word = lemmatizer.lemmatize(word)
        #     print(word)
        #     print("==========")
        word = lemmatizer.lemmatize(word)

        if word in weird_plurals.keys():
            word = weird_plurals[word]
        lemm_text.append(word)
    text = " ".join(lemm_text)
    return(text)

# Create a list of tuples sorted by index 1 i.e. value field     
def dict_to_top(w_dict, n, reverse=True):
    listofTuples = sorted(w_dict.items() ,reverse=reverse,  key=lambda x: x[1])
    top = {"word":[], "freq":[]}
    rank_dict = {}
    count=0

    # Iterate over the sorted sequence
    for elem in listofTuples :
        if count >n:
            break
        # print(elem[0] , " ::" , elem[1] )
        top["word"].append(elem[0])
        top["freq"].append(elem[1])
        count+=1

    return(top)
# top = dict_to_top(word_dict, 40)

def word_frequency(text_list, stops_dict=False, extra_stops=False, lemm=False):
    word_dict = {}
    text_clean = []

    for text in text_list:
        text = clh.only_letters_clean(text)
        # print(text)
        if lemm==True:
            text = lemmatize_text(text)
        if stops_dict!=False and extra_stops!=False:  
            text = clh.remove_stopword(text, stops_dict, extras=extra_stops)
        word_dict = add_to_freq_dict(text, word_dict) #, lemm=lemm 
        return(word_dict)