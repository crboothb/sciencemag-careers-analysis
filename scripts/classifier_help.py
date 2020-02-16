import string

def no_punctuation(text, quotes=False):
    for mark in string.punctuation:
        if quotes == True:
            if mark == "\"":
                continue
        text = text.replace(mark,"")
    return(text)