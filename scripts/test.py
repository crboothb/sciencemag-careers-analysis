import import_func as imp
import tags_work as tgs
import desc_vis as vis

elist = "../data/editorials-1.jl"
tags = "../data/by_article_110219.jl"

# editorial = imp.import_jl(elist)
tags = imp.import_jl(tags)

# out_edi = imp.process(editorial, "editorial")
out_tag = imp.process(tags, "tags")

# edi_df = out_edi[0]
# edi_dict = out_edi[1]

tag_df = out_tag[0]
tag_dict = out_tag[1]

# print(edi_df.head)
# print(tag_df.head)

# print(len(edi_df))
# print(len(editorial))
# print(len(tag_df))
# print(len(tags))
# print(len(edi_df)-len(tag_df))

# cumulative = imp.cumulative()

# print(cumulative[0])
# print(cumulative[1])

# edi_df = imp.seq_dates(edi_df, "editorial")
tag_df = imp.seq_dates(tag_df, "tags")
print(tag_df.tail(10))

# print(edi_df.head())
# print(tag_df.head())

columns = imp.id_columns(tag_df)
columns = tgs.seperate_tags(columns)

inc_dict = tgs.tag_incidence(columns, lifespan = True, id_col_tag = True, binary = True)

# col_diffs = tgs.id_column_tags(inc_dict, binary=True)

# print(len(inc_dict))
# print(len(col_diffs))