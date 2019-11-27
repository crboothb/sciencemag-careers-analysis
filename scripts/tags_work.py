## code for working with article tags

import pandas as pd
import sys

import import_func as imp


# first, need to tidy data by putting all the tags into their own rows,
# keeping the article data affiliated with each tag
# function takes dataframe
# the dataframe must contain a column titled "tags" with its values as a series of lists of tags

def seperate_tags(df):
    heads = [head for head in df.columns.values]
    # print(heads)
    if "tags" not in heads:
        print("seperate_tags function requires a tags column")
    else:
        heads.remove('tags')
        # print(heads)

        tags_seperate = df.tags.apply(pd.Series) \
            .merge(df, left_index = True, right_index = True) \
            .drop(["tags"], axis = 1) \
            .melt(id_vars = heads, value_name = "tag") \
            .dropna()

    return(tags_seperate)

def tag_incidence(df):
    # Still a work in progress in Text_Analysis2
    inc_dict = {}

    for i in range(600,700):
        w_tag = df.loc[i, "tag"]
        w_author = df.loc[i, "authors"]
        if w_tag in inc_dict.keys():
            if w_author in inc_dict[w_tag].keys():
                inc_dict[w_tag][w_author] += 1
            else:
                inc_dict[w_tag][w_author] = 1
        else:
            inc_dict[w_tag] = {}
            inc_dict[w_tag][w_author] = 1

    # for key in inc_dict.keys():
    #     print(key, inc_dict[key])
    return(inc_dict)