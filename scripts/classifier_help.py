import re
import string

import pandas as pd


def no_punctuation(text, quotes=False):
    for mark in string.punctuation:
        if quotes is True:
            if mark == '"':
                continue
        text = text.replace(mark, "")
    return text


def replace_quotes(text):
    # text = text.replace("\“","\"")

    quotes = re.findall(r"\"(.+?)\"", text)

    to_replace = quotes

    for quote in to_replace:
        text = text.replace(quote, " QUOTATION_REPLACEMENT ")
        # print(quote+"\n")
    return text


def count_pro(clean_text, person):
    if person == "first":
        pronouns = [" i ", " im ", " ive ", " id ", " my ", " me ", " myself "]
    elif person == "second":
        pronouns = [" you ", " youre ", " youve ", " youd ", " your ", " yourself "]
    else:
        pronouns = []

    count = 0

    clean_text = replace_quotes(clean_text)

    for pro in pronouns:
        count += clean_text.count(pro)
    return count


def pronouns(f_df, sample="none"):
    first_pronouns = [" i ", " im ", " ive ", " id ", " my ", " me ", " myself "]
    second_pronouns = [" you ", " youre ", " youve ", " youd ", " your ", " yourself "]
    # third_pronouns = []

    if sample == "none":
        sample = [i for i in range(len(f_df))]

    counts = {}
    counts4df = {"id": [], "year": [], "first": [], "second": [], "wc": []}

    for samp in sample:
        count1 = 0
        count2 = 0
        try:
            w_text = no_punctuation(f_df["text"][samp], quotes=True)
        except:
            continue
        w_text = replace_quotes(w_text)
        w_text = no_punctuation(w_text, quotes=False)
        for pro in first_pronouns:
            count1 += w_text.count(pro)
        for pro in second_pronouns:
            count2 += w_text.count(pro)
        wc = len(w_text.split(" "))
        counts[samp] = {"first": count1, "second": count2, "wc": wc}
        counts4df["id"].append(samp)
        counts4df["year"].append(f_df["year"][samp])
        counts4df["first"].append(count1)
        counts4df["second"].append(count2)
        counts4df["wc"].append(wc)

    c_df = pd.DataFrame(counts4df)
    return c_df


def category(df):
    category_codes = {1: "first", 2: "second", 3: "third"}

    df["Category"] = df["Category_Code"]
    df = df.replace({"Category": category_codes})
    df = df.rename(columns={"category": "Category_Code"})
    return df
