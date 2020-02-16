import string
import re

def no_punctuation(text, quotes=False):
    for mark in string.punctuation:
        if quotes == True:
            if mark == "\"":
                continue
        text = text.replace(mark,"")
    return(text)

def replace_quotes(text):
    text = text.replace("\“","\"")

    quotes = re.findall(r'\"(.+?)\"', text)

    to_replace = quotes
    
    for quote in to_replace:
        text = text.replace(quote," QUOTATION_REPLACEMENT ")
        # print(quote+"\n")
    return(text)

