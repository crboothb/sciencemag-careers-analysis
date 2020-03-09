# Generate stable samples for code_interface

import pickle
import random
import pandas as pd
import import_func as imp
import numpy as np

full_filename = "../data/by_article_fulltext_020920.jl"

path_df = "pickles/sample200.pickle"

with open(path_df, "rb") as data:
    old_sample = pickle.load(data)


full_dict = imp.init_df(full_filename, "full", "df")


def drop_short(df):
    to_drop = []
    for i in df.index.values:
        # print(i)
        text = df.loc[i, "text"]
        if len(text.split(" ")) < 200:
            # print(i)
            to_drop.append(i)

    # print(to_drop)
    return df.drop(to_drop)


full_dict = drop_short(full_dict)


# print("###########################")
# for key in full_dict.keys():
#     print(len(full_dict[key]))

print("data loaded")

possible_vals = full_dict.index.values
# print(type(possible_vals), type(old_sample))
possible_vals_wo = np.delete(possible_vals, old_sample)
# print(len(possible_vals)-len(possible_vals_wo))

sample200 = random.sample(list(possible_vals), 200)

# This function creates chunks and returns them
def chunkify(lst, n):
    return [lst[i::n] for i in [j for j in range(n)]]


sample200_chunks = chunkify(sample200, 10)

for chunk in sample200_chunks:
    print(chunk)

with open("pickles/sample200-2.pickle", "wb") as output:
    pickle.dump(sample200, output)

with open("pickles/sample200-2_chunks.pickle", "wb") as output:
    pickle.dump(sample200_chunks, output)
