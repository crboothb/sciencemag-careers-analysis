## code for working with article tags

import pandas as pd
import sys
import numpy as np

import import_func as imp


# first, need to tidy data by putting all the tags into their own rows,
# keeping the article data affiliated with each tag
# function takes dataframe
# the dataframe must contain a column titled "tags" with its values as a series of lists of tags

def seperate_tags(df):
    heads = [head for head in df.columns.values]
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

# first this function requires the separate_tags dataframe--it will call it if necessary
# takes dataframe, takes lifespan as arguments
# if lifespan = True 
# returns a dictionary

# structure of inc_dict
# {tag: 
#     {"overall":
#         "total": int,
#         "span": [[date_seq,month_seq] [date_seq, month_seq],...],
#         "col_tag?": int OR "yes"/"no"
#     }
#     {"author1": int, "author2": int, ... }
# }

def tag_incidence(df, lifespan = True, id_col_tag = False, quantile = .8, binary = True):

    i_dict = {}

    for i in df.index.values:
        # print(df.loc[i, "authors"]," ", df.loc[i, "tag"])
        w_tag = df.loc[i, "tag"]
        w_author = df.loc[i, "authors"]
        if w_tag in i_dict.keys():
            i_dict[w_tag]["overall"]["total"] += 1
            if w_author in i_dict[w_tag].keys():
                i_dict[w_tag][w_author] += 1
            else:
                i_dict[w_tag][w_author] = 1
        else:
            i_dict[w_tag] = {}
            i_dict[w_tag]["overall"] = {}
            i_dict[w_tag]["overall"]["total"] = 1
            if lifespan == True:
                i_dict[w_tag][w_author] = 1
                i_dict[w_tag]["overall"]["span"] = []
            else:
                i_dict[w_tag][w_author] = 1
        if lifespan == True:
            i_dict[w_tag]["overall"]["span"].append([df.loc[i, "date_seq"],df.loc[i, "month_seq"]])
    if id_col_tag == True:
        test = id_column_tags(i_dict, quantile = quantile, binary = binary)
        for key in [key for key in test.keys()]:
            i_dict[key]["overall"]["col_tag"] = test[key]
        return(i_dict)

    else:
        return(i_dict)

# 

##  Possible strategies
# max(prop of author) - (number of authors/incidence) = diff
# ----> if diff is higher, it's more likely to be a column tag for a

def id_column_tags(i_dict, quantile = .8, binary = True):
    col_tag = {}

    for key in i_dict.keys():
        tot = i_dict[key]["overall"]["total"]
        prop_author = []
        for author in i_dict[key].keys():
            if author == "overall":
                continue
            else:
                prop_author.append(i_dict[key][author]/tot)
        col_tag[key] = [i_dict[key]["overall"]["total"]]
        col_tag[key].append(prop_author)

    diff_set = []
    out_col_tag = {}

    for key in col_tag.keys():
        if len(col_tag[key][1]) == 1:
            diff = max(col_tag[key][1]) - len(col_tag[key][1])/col_tag[key][0]
        # elif len(col_tag[key][1]) < 4:
        #     diff = max(col_tag[key][1]) - len(col_tag[key][1])/col_tag[key][0]
        else:
            diff = max(col_tag[key][1])
        if binary == False:
            out_col_tag[key] = diff
        else:
            col_tag[key].append(diff)
            diff_set.append(diff)

    if binary == True:
        q = np.quantile(diff_set, quantile)
        for key in col_tag.keys():
            if col_tag[key][2] > q:
                out_col_tag[key] = "yes"
            else:
                out_col_tag[key] = "no"

    return(out_col_tag)



