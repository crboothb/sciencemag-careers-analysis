import pandas as pd
import ast
import re
import numpy as np
import sys

sys.path.append('../scripts/')
import import_func as imp
# import tags_work as tgs
# import desc_vis as vis

# something a warning told me to do?
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_colwidth', 100)
# pd.set_option('display.width', 150)

infile = "../data/by_article_fulltext_020920.jl"
outfile = "../data/initial_processed.csv"

full_df = imp.init_df(infile, "full", genre="none", categories="all")

full_df = full_df.drop(
    [
        "date",
        "id",
        "time",
        "date_seq",
        "column1",
        "column2",
        "one_time",
        "bio",
        "authors",
        "headline",
        "n_posts_author",
        "author",
        "category",
    ],
    axis=1,
)


print("data process done")

# print([col for col in full_df.columns])

full_df.to_csv(outfile, index=False)


