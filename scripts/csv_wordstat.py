import csv
import sys

import numpy as np
from langdetect import detect

# import desc_vis as vis
# import classifier_func as cla
import classifier_help as clh
import import_func as imp
import tags_work as tgs

full_advice = "../data/genre_advice_full_021520.jl"
full_filename = "../data/by_article_fulltext_020920.jl"

# advice_df = imp.init_df(full_advice, "full", advice=True)
# advice_df = advice_df[advice_df["year"]<2020]

full_df = imp.init_df(full_filename, "full", categories="limited")
full_df = full_df[full_df["year"] < 2020]

# print(full_df.head())


full_df["type"] = np.where(
    (full_df["working_life"] == "yes"),
    "working_life",
    np.where(
        (full_df["career_related_policy"] == "yes"),
        "career_related_policy",
        np.where(
            (full_df["advice"] == "yes"),
            "advice",
            np.where(
                (full_df["career_profiles"] == "yes"),
                "career_profiles",
                "uncategorized",
            ),
        ),
    ),
)

full_df = full_df.drop(
    [
        "date",
        "time",
        "date_seq",
        "column1",
        "column2",
        "one_time",
        "working_life",
        "career_related_policy",
        "career_profiles",
        "bio",
    ],
    axis=1,
)

print(full_df.tail())
# print(full_df.tail())
print(full_df.columns)

# filter out articles that aren't in English
# print(len(full_df))
# full_df["lang"] = ["en" if detect(x) == "en" else "no" for x in full_df["text"]]
# full_df = full_df[full_df.lang == "en"]
# print("include only english articles")
# print(len(full_df))

# filter out articles with less than 200 words
print(len(full_df))
full_df["word_count"] = [len(x) for x in full_df["text"]]
full_df = full_df[full_df.word_count > 200]
print("include only articles with <200 words")
print(len(full_df))


# full_df = full_df.drop(["lang", "word_count"], axis=1,)

sys.exit()
# full_df.to_csv("../data/full_raw.csv", index=False)

full_df["no_quotes"] = [clh.replace_quotes(text) for text in full_df["text"]]
full_df_q = full_df.drop(["text"], axis=1,)

# full_df_q.to_csv("../data/full_no_quote.csv", index=False)

# full_df = cla.clean_text_df(full_df)
# full_df_c = full_df.drop(["text", "no_quotes"], axis=1,)

# full_df_c.to_csv("../data/full_clean.csv", index=False)

# print("clean 1 done")

# full_df = cla.clean_text_df(full_df, col="no_quotes")
# full_df_c_nq = full_df.drop(["text", "no_quotes", "text_Parsed"], axis=1,)
# full_df_c_nq.to_csv("../data/full_clean_no_quote.csv", index=False)

# # print(full_df.head(20))

# print(full_df.columns)
