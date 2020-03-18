import csv
from langdetect import detect

import import_func as imp
import tags_work as tgs
# import desc_vis as vis
import classifier_func as cl
import classifier_help as clh

full_advice = "../data/genre_advice_full_021520.jl"
full_filename = "../data/by_article_fulltext_020920.jl"

# advice_df = imp.init_df(full_advice, "full", advice=True)
# advice_df = advice_df[advice_df["year"]<2020]

full_df = imp.init_df(full_filename, "full")
full_df = full_df[full_df["year"]<2020]
print(len(full_df))
full_df["lang"] = ["en" if detect(x) == "en" else "no" for x in full_df["text"]]
full_df = full_df[full_df.lang == "en"]
print(len(full_df))

for i in range(5):
    print(detect(full_df["text"][i]))

# full_df["advice"] = ["yes" if "advice" in x else "no" for x in full_df["tags"]]

# full_df["no_quotes"] = [clh.replace_quotes(text) for text in full_df["text"]]
# full_df = cl.clean_text_df(full_df)
# print("clean 1 done")
# full_df = cl.clean_text_df(full_df, col="no_quotes")

full_df = full_df.drop(
    [
        "date",
        "time",
        "date_seq",
        "lang"
        # "text"
    ],
    axis=1,
)

# print(full_df.head(20))

# print(full_df.columns)

# full_df.to_csv("../data/full_no_quote.csv", index=False)
# full_df.to_csv("../data/full_no_quote.csv", index=False)