## functions for pre-visualization table manipulation

import pandas as pd

# prepare data for sns density plots
# this takes a list of 2 datasets

def prep_per_month(df1):

    df = editorial.groupby("month_seq").sum()
    #df.head(30)
    df["month_seq"] = df.index   

    y_seq = []
    for n_months in df["month_seq"]:
        for months in cumulative_months:
            if n_months < months:
                year = cumulative_months.index(months)
                y_seq.append(year + 1996)
                break
    df["year"] = y_seq
    df.head()