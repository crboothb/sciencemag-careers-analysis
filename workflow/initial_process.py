import pandas as pd
import sys

sys.path.append('../scripts/')
import import_func as imp

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

full_df.to_csv(outfile, index=False)


