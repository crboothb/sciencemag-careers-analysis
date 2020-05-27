import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 

def only_letters_clean(text):
    valids = re.sub(r"[^A-Za-z ]+", '', text)
    return(valids)

def no_punctuation(text, quotes=False, frequency_prep=False):
    text = str(text)
    for mark in string.punctuation+"--”":
        if quotes is True:
            if mark == '"':
                continue
            text = text.replace(mark, "")
        if frequency_prep == True:
            if mark == "-":
                text.replace(mark, " ")
                continue
            if mark == "'":
                text = text.replace(mark, "")
                continue
            text = text.replace(mark, " ")
        else:
            text = text.replace(mark, "")
    return text

def remove_stopword(text, stops_dict, extras=[]):
    bow = text.strip().split(" ")
    new_bow = []
    for word in bow:
        if word not in stops_dict and word not in extras:
            new_bow.append(word)
    return(" ".join(new_bow))

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