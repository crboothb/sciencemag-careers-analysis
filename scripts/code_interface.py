# too annoying in jupyter notebooks

import pickle
import pandas as pd
import re
import string
import random

import import_func as imp
import tags_work as tgs
import desc_vis as vis

session = 10
full_filename = "../data/by_article_fulltext_020920.jl"

# get full text dataset as a df
# full_df = imp.init_df(full_filename, "full")

# get full dataset as a dict
# full_dict = imp.init_df(full_filename, "full", "dict") # Apparently this still returns a pandas dataframe... Awkward
full_dict = imp.init_df(full_filename, "full", "df") # This variable is still saved as full_dict so that I don't have to change the rest of the variables
# print(full_dict.keys())
# print(full_df.head())

# print(full_dict.head())

# for key in full_dict.keys():
#     print(len(full_dict[key]))

def drop_short(df):
    to_drop = []
    for i in df.index.values:
        # print(i)
        text = df.loc[i, "text"]
        if len(text.split(" ")) < 200:
            # print(i)
            to_drop.append(i)

    # print(to_drop)
    # df = df.drop(to_drop)
    return(df.drop(to_drop))

full_dict = drop_short(full_dict)

# print("###########################")
# for key in full_dict.keys():
#     print(len(full_dict[key]))

print("data loaded")

# print(type(full_dict.index.values))
# sample200 = random.sample(list(full_dict.index.values), 200)
# sample200_chunks = []

with open("pickles/sample200.pickle", 'rb') as data:
    sample200 = pickle.load(data)

with open("pickles/sample200_chunks.pickle", 'rb') as data:
    sample200_chunks = pickle.load(data)


# sample50 = [3188, 1591, 2152, 4044, 2789, 5685, 5191, 2360, 518, 189, 5509, 3033, 499, 2024, 3563, 4216, 1422, 3904, 3256, 420, 4940, 3397, 6087, 4548, 227, 4817, 1351, 765, 4161, 5139, 4899, 5243, 1334, 4234, 2629, 815, 5516, 2170, 1765, 3183, 5143, 3225, 1759, 5209, 5249, 4487, 3447, 4963, 2656, 825]
# sample_t = [2,4,300,8]



# functions
def no_punctuation(text, quotes=False):
    for mark in string.punctuation:
        if quotes == True:
            if mark == "\"":
                continue
        text = text.replace(mark,"")
    return(text)

test = no_punctuation(full_dict["text"][5])


def replace_quotes(text, flag="false", error="false", right="false"):
    text = text.replace("\“","\"")
    count = error

    quotes = re.findall(r'\"(.+?)\"', text)

    to_replace = quotes


    for quote in to_replace:
        text = text.replace(quote," QUOTATION_REPLACEMENT ")
        # print(quote+"\n")
    if type(error) == int:
        right += len(quotes)
        return(text, count, right)
    else:
        return(text)

def count_pro(clean_text, person):
    if person == "first":
        pronouns = [" i "," im ", " ive ", " id "," my ", " me ", " myself "]
    elif person == "second":
        pronouns = [" you "," youre ", " youve "," youd "," your ", " yourself "]
    else:
        pronouns = []
    
    count = 0

    clean_text = replace_quotes(clean_text)

    for pro in pronouns:
        count += clean_text.count(pro)
    return(count)


counts4df = {"id":[],"first":[],"second":[],"wc":[],"first_f":[],"second_f":[], "input":[]}

count = 0

for num in sample200_chunks[session-1]:
    count+=1
    text = full_dict["text"][num]
    wc = len(text.split(" "))
    # print(num)
    # print(count_pro(text, "first")/wc)
    # print(count_pro(text, "second")/wc)
    print("\n\n"+str(count))
    print(text)
    advance = input("any key")
    counts4df["id"].append(num)
    # counts4df["year"].append(f_df["year"][samp])
    counts4df["first"].append(count_pro(no_punctuation(text, quotes=True), "first"))
    counts4df["second"].append(count_pro(no_punctuation(text, quotes=True), "second"))
    counts4df["wc"].append(wc)
    counts4df["first_f"].append(count_pro(no_punctuation(text, quotes=True), "first")/wc)
    counts4df["second_f"].append(count_pro(no_punctuation(text, quotes=True), "second")/wc)
    counts4df["input"].append(advance)

hand_coded_df_20_1 = pd.DataFrame(counts4df)

# print(hand_coded_df)

with open('pickles/hand_coded'+str(session)+'.pickle', 'wb') as output:
    pickle.dump(hand_coded_df_20_1, output)

print("done")
