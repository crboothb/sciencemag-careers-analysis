import pandas as pd
import matplotlib as plt
import numpy as np
import seaborn as sns
import sys

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

sys.path.append('../scripts/')
import import_func as imp
import classifier_help as clh

#################
### functions ###
#################



#################


infile = "../data/initial_processed.csv"
outfig_inc = "../figs/tag_bargraph.png"
outfileR = "../data/bargraph_data/tag_bargraph_data"
outfileRall = "../data/bargraph_data/all_bargraph_data"

################

legend_dict ={}
legend_cats = [
    "advice",
    "job market",
    "academic",
    "workplace diversity",
    "non-disciplinary",
    "postdoc",
    "graduate",
    "midcareer",
    "life and career balance",
    "industry",
    "career profiles",
    "government",
    "undergraduate",
    "working life",
    "early career",
    "career-related policy"
        ]


categories = []
for tag in legend_cats:
    cat = tag.replace(" ", "_").replace("-", "_")
    categories.append(cat)
    legend_dict[cat] = tag


full_df = pd.read_csv(infile)

# averages overall

# first_overall = []
# second_overall = []

pieces = []

for cat in categories:
    cat_df = full_df[full_df[cat] == "yes"]
    # print(len(cat_df))
    # print(len(counts_df))

    ###########
    # counts_df = clh.pronouns(cat_df)

    # counts_df["frac1"] = counts_df["first"]/counts_df["wc"]
    # counts_df["frac2"] = counts_df["second"]/counts_df["wc"]


    ###########
    # counts_df = clh.modals(cat_df)

    # counts_df["frac"] = counts_df["modals"]/counts_df["wc"]

    ###########
    counts_df = clh.hedges(cat_df, "hedges")
    counts_b_df = clh.hedges(cat_df,"boosters")

    counts_df["frac_h"] = counts_df["hedges"]/counts_df["wc"]
    counts_df["frac_b"] = counts_b_df["boosters"]/counts_df["wc"]

    pieces.append(counts_df)

all_tag = pd.concat(pieces, keys=[cat for cat in categories])
all_tag = all_tag.reset_index()

all_tag.to_csv(outfileR+"_hedges.csv", index=False)

counts_df = clh.pronouns(full_df)

counts_df["frac1"] = counts_df["first"]/counts_df["wc"]
counts_df["frac2"] = counts_df["second"]/counts_df["wc"]

counts_df.to_csv(outfileRall+"_hedges.csv", index=False)


