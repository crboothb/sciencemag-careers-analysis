# Generate stable samples for code_interface

import random
import pickle
import pandas as pd

import import_func as imp



full_filename = "../data/by_article_fulltext_112919-2.jl"

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
    return(df.drop(to_drop))

full_dict = drop_short(full_dict)


# print("###########################")
# for key in full_dict.keys():
#     print(len(full_dict[key]))

print("data loaded")


sample200 = random.sample(list(full_dict.index.values), 200)

# This function creates chunks and returns them
def chunkify(lst,n):
    return([ lst[i::n] for i in [j for j in range(n)] ])
 
sample200_chunks = chunkify(sample200, 10)

for chunk in sample200_chunks:
    print(chunk)

with open('pickles/sample200.pickle', 'wb') as output:
    pickle.dump(sample200, output)

with open('pickles/sample200_chunks.pickle', 'wb') as output:
    pickle.dump(sample200_chunks, output)