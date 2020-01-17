## code for working with article tags

import pandas as pd
import sys
import numpy as np

import import_func as imp


# first, separate tags tidies the data by putting all the tags into their own rows,
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

# first tag_incidence requires the usual dataframe after imp.init_df processing
# it will call the separate_tags function on its own
# takes dataframe, takes lifespan as arguments
# if lifespan = True 
# if dict_return = True, it returns a dictionary.
# Otherwise, it returns a dataframe by default

# structure of inc_dict
# {tag: 
#     {"overall":
#         "total": int,
#         "span": [[date_seq,month_seq] [date_seq, month_seq],...],
#         "col_tag?": int OR "yes"/"no"
#     }
#     {"author1": int, "author2": int, ... }
# }

def tag_incidence(df, lifespan = True, id_col_tag = False, quantile = .8, binary = True, dict_return=False):
    df = seperate_tags(df)

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
        if dict_return == True:
            return(i_dict)

    else:
        if dict_return == True:
            return(i_dict)

    # convert dictionary to dataframe
    if dict_return == False:
        col_tag_todf = {}

        for i in df.index.values:
            w_tag = df.loc[i, "tag"]
            col_tag_todf[w_tag] = i_dict[w_tag]["overall"]["col_tag"]

        df["col_tag"] = df["tag"].map(col_tag_todf) 
        return(df)


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

def inc_per_year(i_dict):
    # tags incidence dataframe
    tag_inc_df = {"year":[],"tag":[],"incidence":[]}
    tag_inc_counting = {}
    # tag_inc_counting = {tag: {year:int, year: int, year: int}}

    # count incidences of each tag per year
    for key in [key for key in i_dict.keys()]:
        # print(key)
        if i_dict[key]["overall"]["col_tag"] == "no": # filter out tags that are probs identifying columns
            if key in tag_inc_counting.keys():
                for post in i_dict[key]["overall"]["span"]:
                    w_year = imp.cumul_to(post[1], "m")
                    print(w_year)
                    if w_year in tag_inc_counting[key].keys():
                        print("add2")
                        tag_inc_counting[key][w_year] += 1
                    else:
                        tag_inc_counting[key][w_year] = 1
                        print(tag_inc_counting[key])
            else:
                tag_inc_counting[key] = {}
                for post in i_dict[key]["overall"]["span"]:
                    w_year = imp.cumul_to(post[1], "m")
                    #print(w_year)
                    if w_year in tag_inc_counting[key].keys():
                        #print("add1")
                        tag_inc_counting[key][w_year] += 1
                    else:
                        tag_inc_counting[key][w_year] = 1
                        #print(tag_inc_counting[key])

    # convert counting dictionary to dictionary that can be made into a df
    for key in tag_inc_counting.keys():
        for year in tag_inc_counting[key].keys():
            tag_inc_df["year"].append(year)
            tag_inc_df["tag"].append(key)
            tag_inc_df["incidence"].append(tag_inc_counting[key][year])

    tag_inc_df = pd.DataFrame(tag_inc_df)
    return(tag_inc_df)
