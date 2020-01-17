import import_func as imp
import tags_work as tgs
import desc_vis as vis
import seaborn as sns
import matplotlib as plt
import random

elist_filename = "../data/editorials-1.jl"
tags_filename = "../data/by_article_110219.jl"
full_filename = "../data/by_article_fulltext_112919-2.jl"
test_full_filename = "../data/full_text.jl"

# def init_df(filename, focus, test = False):
#     raw = imp.import_jl(filename)
#     out = imp.process(raw, focus = focus, out_form = "df")

#     df = out
#     df = imp.seq_dates(df, focus)
#     if focus != "editorial":
#         df = imp.id_columns(df)
#     if test == True:
#         print(df.head())
#     return(df)

## to import ##

# tag_df = imp.init_df(tags_filename, "tags")
# edi_df = imp.init_df(elist_filename, "editorial")
full_df = imp.init_df(full_filename, "full")

###########

## to mess around with tag incidence functions

tags_dict_id = tgs.tag_incidence(full_df, lifespan = True, id_col_tag = True, binary = True, dict_return=True)
year_inc = tgs.inc_per_year(tags_dict_id)

print(tags_dict_id["oncology"])
print(year_inc.tail(20))


###########

## to import and examine full text ##

# full = imp.import_jl(full)
# out_full = imp.process(full, focus = "full", out_form = "dict")
# full_dict = out_full

# print(out_full["headline"][0])
# print(out_full["tags"])
# print(out_full["authors"])
# print(out_full["date"])
# print(out_full["time"])
# print(len(out_full["text"]))
# print(len(out_full["bio"]))

# sample = [random.randint(1, len(full)) for j in range(20)]
# # sample = [4399, 132, 310, 3442, 930, 135, 1532, 162, 1077, 3073, 4762, 5464, 5989, 4457, 2713, 1592, 3898, 3326, 3030, 3247]

# for i in sample:
#     print("\n\n#######\n\n")
#     print(out_full["date"][i])
#     print(out_full["text"][i])

# print(out_full["text"][0][0])  
# print("#####") 

###########

## for calling and testing number of posts over time graphs

# per_month_df = vis.prep_per(tag_df, group_by = "year", test = True)

# column = vis.dual_per(tag_df, split = "column2", group_by = "avg_month", test = True)

# column1 = column[0][0]
# column2 = column[1][0]

# column_df0 = vis.prep_per(column1, group_by = "year", color = "red", test = False)
# column_df1 = vis.prep_per(column2, group_by = "year", color = "blue", test = False)

# sns.lineplot(x = "year", y = "n", color = "red", data = column_df0) 
# sns.lineplot(x = "year", y = "n", color = "blue", data = column_df1) 
# plt.pyplot.show()


###########


# print(edi_df.head)
# print(tag_df.head)

# print(len(edi_df))
# print(len(editorial))
# print(len(tag_df))
# print(len(tags))
# print(len(edi_df)-len(tag_df))


# edi_df = imp.seq_dates(edi_df, "editorial")

# inc_dict = tgs.tag_incidence(columns, lifespan = True, id_col_tag = True, binary = True)

# col_diffs = tgs.id_column_tags(inc_dict, binary=True)

# print(len(inc_dict))
# print(len(col_diffs))