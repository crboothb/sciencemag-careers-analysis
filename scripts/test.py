import import_func as imp
import desc_vis as vis
import seaborn as sns

elist = "../data/editorials-1.jl"
tags = "../data/by_article_110219.jl"

editorial = imp.import_jl(elist)
tags = imp.import_jl(tags)

out_edi = imp.process(editorial, "editorial")
out_tag = imp.process(tags, "tags")

edi_df = out_edi[0]
edi_dict = out_edi[1]

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

edi_df = imp.seq_dates(edi_df, "editorial")
tag_df = imp.seq_dates(tag_df, "tags")

# print(edi_df.head())
# print(tag_df.head())

authors_test = imp.id_columns(tag_df, 5)

print(authors_test.head(10))