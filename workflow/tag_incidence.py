import sys
import pandas as pd
import ast
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

sys.path.append('../scripts/')
import import_func as imp
import desc_vis as vis

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

### functions ###

def output_plot(outfile):
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig(outfile, dpi=100)

#################


infile = "../data/initial_processed.csv"
outfig_inc = "../figs/article_types_expanded.png"
outfig_avgtags = ""

full_df = pd.read_csv(infile)

# print(full_df.head())

legend_categories = [
    "advice",
    "job market",
    "academic",
    "postdoc",
    "graduate",
    "workplace diversity",
    "midcareer",
    "non-disciplinary",
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
for cat in categories:
    cat = cat.replace(" ", "_").replace("-", "_")
    categories.append(cat)

colors = [
    "#000000",
    "#9D9D9D",
    "orange",
    "#BE2633",
    "#E06F8B",
    "#493C2B",
    "#A46422",
    "#EB8931",
    "#F7E26B",
    "#2F484E",
    "#44891A",
    "#A3CE27",
    "#1B2632",
    "#005784",
    "#31A2F2",
    "#B2DCEF"
]

brights = [
    
]

grays = [
    
]

bold_cats = [
    "advice",
    "job_market",
    "academic",
    "non_disciplinary",
    "workplace_diversity"
]

##################

# all posts visualization

full_vis = vis.prep_per(full_df, group_by = "year", color = "red", test = False)

plots = []
count=0

plt.figure(figsize=(12, 8))
for cat in categories:
    if cat in bold_cats:
        boldness=4
    else:
        boldness=2
    cat_df = full_df[full_df[cat] == "yes"]
    cat_vis = vis.prep_per(cat_df, group_by = "year")
    # plt.plot(
    #     "year", "n", data = cat_vis,
    #     color = colors[count],
    #     linewidth=boldness,
    #     legend="full", label=legend_categories[count]
    #     )
    # plt.show()
    sns.lineplot(
        x = "year", y = "n", color = colors[count],
        legend="full", label=legend_categories[count],
        linewidth=boldness,
        data = cat_vis
        )
    # plt.show()

    count+=1

# sns.lineplot(x = "year", y = "n", color = "red", legend="full", label="all articles",data = full_vis)
# plt.title("Category articles by year over time")
# plt.show()
output_plot("../figs/article_types_expanded.png")

