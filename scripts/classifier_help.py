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


def pronouns(f_df, sample="none", q_replace=True):
    first_pronouns = [" i ", " im ", " ive ", " id ", " my ", " me ", " myself "]
    second_pronouns = [" you ", " youre ", " youve ", " youd ", " your ", " yourself "]
    # third_pronouns = []

    if sample == "none":
        sample = [i for i in range(len(f_df))]

    counts = {}
    counts4df = {"id": [], "year": [], "month_seq":[], "first": [], "second": [], "wc": []}

    for samp in sample:
        count1 = 0
        count2 = 0
        try:
            w_text = no_punctuation(f_df.iloc[samp]["text"], quotes=True)
        except:
            continue
        if q_replace == True:
            w_text = replace_quotes(w_text)
        w_text = no_punctuation(w_text, quotes=False)
        for pro in first_pronouns:
            count1 += w_text.count(pro)
        for pro in second_pronouns:
            count2 += w_text.count(pro)
        wc = len(w_text.split(" "))
        counts[samp] = {"first": count1, "second": count2, "wc": wc}
        counts4df["id"].append(samp)
        counts4df["year"].append(f_df.iloc[samp]["year"])
        counts4df["month_seq"].append(f_df.iloc[samp]["month_seq"])
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


def modals(f_df, sample="none"):
    modal_list = [
        " can ",
        " could ",
        " cant ",
        " couldnt ",
        " may ",
        " might ",
        " shall ",
        " should ",
        " shouldnt ",
        " will ",
        " would ",
        " wont ",
        " wouldnt ",
        " must ",
        " ought ",
        " had better ",
        " have to ",
    ]
    # third_pronouns = []

    if sample == "none":
        sample = [i for i in range(len(f_df))]

    counts = {}
    counts4df = {"id": [], "year": [], "month_seq":[], "modals": [], "wc": []}

    for samp in sample:
        count = 0
        try:
            w_text = no_punctuation(f_df.iloc[samp]["text"], quotes=True)
        except:
            continue
        w_text = replace_quotes(w_text)
        w_text = no_punctuation(w_text, quotes=False)
        for verb in modal_list:
            count += w_text.count(verb)
        wc = len(w_text.split(" "))
        counts[samp] = {"modals": count, "wc": wc}
        counts4df["id"].append(samp)
        counts4df["year"].append(f_df.iloc[samp]["year"])
        counts4df["month_seq"].append(f_df.iloc[samp]["month_seq"])
        counts4df["modals"].append(count)
        counts4df["wc"].append(wc)

    c_df = pd.DataFrame(counts4df)
    return c_df


def hedges(f_df, hedges, sample="none", q_replace=True):

    if hedges == "hedges":
        infile = "../data/hedges.csv"
    elif hedges == "boosters":
        infile = "../data/boosters.csv"
    else:
        print("input hedges attribute as either hedges or boosters")

    h_list = [" " + word[:-1] + " " for word in open(infile, "r")]
    # print(h_list[:10])
    # third_pronouns = []

    if sample == "none":
        sample = [i for i in range(len(f_df))]

    counts = {}
    counts4df = {"id": [], "year": [], "month_seq":[], hedges: [], "wc": []}

    for samp in sample:
        count = 0
        try:
            w_text = no_punctuation(f_df.iloc[samp]["text"], quotes=True)
        except:
            continue
        if q_replace == True:
            w_text = replace_quotes(w_text)
        w_text = no_punctuation(w_text, quotes=False)
        for verb in h_list:
            count += w_text.count(verb)
        wc = len(w_text.split(" "))
        counts[samp] = {"modals": count, "wc": wc}
        counts4df["id"].append(samp)
        counts4df["year"].append(f_df.iloc[samp]["year"])
        counts4df["month_seq"].append(f_df.iloc[samp]["month_seq"])
        counts4df[hedges].append(count)
        counts4df["wc"].append(wc)

    c_df = pd.DataFrame(counts4df)
    return c_df
