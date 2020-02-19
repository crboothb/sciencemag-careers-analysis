## functions for pre-visualization table manipulation

import numpy as np
import pandas as pd

import import_func as imp

# prepare data for sns density plots
# this takes one dataset
# requires the data to be procesed with imp.seq_dates() to have sequential months and years


def prep_per(df, group_by="avg_month", color="blue", test=False):
    import seaborn as sns
    import matplotlib as plt

    df["n"] = 1

    if group_by == "month":
        w_x = "month_seq"
    elif group_by == "avg_month" or group_by == "year":
        w_x = "year"
    else:
        print("argument group_by takes 'month', 'avg_month', or 'year'")

    if group_by == "month" or group_by == "avg_month":
        df = df.groupby("month_seq").sum()
        if group_by == "avg_month":
            df = df.groupby("year").sum() / 12
    elif group_by == "year":
        df = df.groupby("year").sum()

    # df[w_x] = df.index
    df = df.reset_index()

    if test is True:
        print(df.head())
        sns.lineplot(x=w_x, y="n", color=color, data=df)
        plt.pyplot.show()
    return df


def dual_per(df, split, test=False):  # group_by,
    if split == "column2":
        vals = df.column2.unique()
    # colors = ["red", "blue"]
    w_dfs = []
    # order = []
    for i in range(len(vals)):
        # order.append(vals[i])
        if split == "column2":
            w_df = df[df.column2 == vals[i]]
        # w_df = prep_per(w_df, group_by, test, colors[i])

        # print([w_df.head(), vals[i]])
        w_dfs.append([w_df, vals[i]])

    return w_dfs
